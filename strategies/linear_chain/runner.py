"""
Orquestador de la estrategia de evaluación secuencial (Linear Chain).

Este módulo define el `LinearChainRunner`, que implementa una cadena de
responsabilidad predefinida y secuencial para procesar una consulta de
usuario de principio a fin, aplicando una lógica de "fail-fast".
"""

import time
from typing import Final

from core.providers import provider as llm_provider
from schema import ExecutionReport, TraceStep
from strategies.linear_chain.components.bq_connector import BQConnector
from strategies.linear_chain.components.data_interpreter import DataInterpreter
from strategies.linear_chain.components.query_validator import QueryValidator
from strategies.linear_chain.components.sql_generator import ArchitectNode


class LinearChainRunner:
    """
    Implementa una estrategia de evaluación secuencial y determinista.

    Orquesta una serie de componentes (Arquitecto, Validador, Conector,
    Intérprete) en un orden fijo. Si un paso intermedio como la validación
    o la ejecución en base de datos falla, la cadena se detiene y se genera
    una respuesta de error controlada.

    Attributes:
        name (str): Nombre identificador de la estrategia.
        architect (ArchitectNode): Componente para generar SQL.
        validator (QueryValidator): Componente para auditar el SQL.
        connector (BQConnector): Componente para ejecutar consultas en BigQuery.
        interpreter (DataInterpreter): Componente para traducir resultados al usuario.
    """

    def __init__(self) -> None:
        """Inicializa todos los componentes necesarios para la cadena secuencial."""
        self._name: Final[str] = "LangChain Sequential"
        self.architect = ArchitectNode(llm_provider)
        self.validator = QueryValidator(llm_provider)
        self.connector = BQConnector()
        self.interpreter = DataInterpreter(llm_provider)

    @property
    def name(self) -> str:
        """Nombre identificador de la estrategia para el benchmark."""
        return self._name

    async def run(self, prompt: str) -> ExecutionReport:
        """
        Ejecuta el flujo completo de la cadena secuencial para un prompt dado.

        El proceso sigue estos pasos:
        1. Generación de SQL por el Arquitecto.
        2. Auditoría de seguridad y semántica por el Validador.
        3. Si la auditoría falla, se interpreta el error y se finaliza (fail-fast).
        4. Ejecución de la consulta en BigQuery por el Conector.
        5. Si la ejecución falla, se interpreta el error y se finaliza (fail-fast).
        6. Interpretación de los datos exitosos para el usuario.

        Args:
            prompt: La consulta del usuario en lenguaje natural.

        Returns:
            ExecutionReport: Un reporte completo con la traza de ejecución,
                latencia total y la respuesta final para el usuario.
        """
        trace: list[TraceStep] = []
        start_total = time.perf_counter()
        final_msg = ""

        # 1. Architect: Genera SQLQuery
        sql_spec, t1 = await self.architect.generate_sql(prompt)
        trace.append(t1)

        # 2. Validator: Audita SQLQuery.raw_sql
        audit_verdict, t2 = await self.validator.audit(prompt, sql_spec.sql)
        trace.append(t2)

        if not audit_verdict.is_safe or not audit_verdict.is_semantically_correct:
            # Fail-fast en caso de fallo de auditoría
            final_msg, t_interpret = await self.interpreter.interpret(
                prompt, audit_verdict.feedback, is_success=False
            )
            trace.append(t_interpret)
        else:
            # 3. Connector: Ejecuta el SQL validado
            data_out, t3 = await self.connector.execute(sql_spec.sql)
            trace.append(t3)

            if data_out.error:
                # Fail-fast en caso de fallo de infraestructura
                final_msg, t_interpret = await self.interpreter.interpret(
                    prompt, data_out.error, is_success=False
                )
                trace.append(t_interpret)
            else:
                # 4. Interpreter: Interpreta la respuesta exitosa
                final_msg, t_interpret = await self.interpreter.interpret(
                    prompt, data_out.data, is_success=True, context=sql_spec.explanation
                )
                trace.append(t_interpret)

        return ExecutionReport(
            strategy_name=self.name,
            output=final_msg,
            latency=time.perf_counter() - start_total,
            trace=trace,
        )
