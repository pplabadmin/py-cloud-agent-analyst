"""
Componente Validador (Auditor) para la cadena de evaluación.

Este módulo define el nodo responsable de interceptar y auditar las consultas SQL
generadas antes de su ejecución. Utiliza un LLM con temperatura 0 para garantizar
evaluaciones deterministas enfocadas en la seguridad (prevención de inyecciones)
y la alineación semántica.
"""

import time
from pathlib import Path
from typing import Any, cast

import yaml
from langchain_core.messages import HumanMessage, SystemMessage

from core.config import settings
from core.providers import LLMProvider
from schema import TraceStep
from strategies.linear_chain.schemas.logic import ValidationVeredict


class QueryValidator:
    """
    Nodo de Auditoría Técnica con tipado estricto y razonamiento vía LLM.

    Actúa como un "gatekeeper" o barrera de seguridad. Evalúa el SQL generado
    contrastándolo con la intención original del usuario y las políticas de
    acceso a datos (solo lectura, tablas permitidas).

    Attributes:
        model: Instancia del LLM configurada con temperatura 0.0 y salida estructurada.
        prompt_path (Path): Ruta absoluta al archivo YAML de configuración del prompt.
        config (dict[str, Any]): Diccionario con las instrucciones del sistema cargadas en memoria.
    """

    def __init__(self, provider: LLMProvider) -> None:
        # Temperatura 0.0 es la mejor práctica para tareas de auditoría/clasificación
        self.model = provider.get_llm(temperature=0.0).with_structured_output(
            ValidationVeredict
        )

        current_file = Path(__file__).resolve()
        self.prompt_path = current_file.parent.parent / "prompts" / "validator.yaml"

        with self.prompt_path.open(encoding="utf-8") as f:
            self.config = cast(dict[str, Any], yaml.safe_load(f))

    async def audit(
        self, user_query: str, generated_sql: str
    ) -> tuple[ValidationVeredict, TraceStep]:
        """
        Audita una consulta SQL generada frente a la intención original del usuario.

        Aplica las reglas de negocio definidas en el prompt del sistema para
        determinar si la consulta es segura (is_safe) y correcta semánticamente
        (is_semantically_correct).

        Args:
            user_query: La pregunta original del usuario en lenguaje natural.
            generated_sql: La consulta SQL generada por el nodo Arquitecto.

        Returns:
            tuple[ValidationVeredict, TraceStep]: El veredicto estructurado de la
                auditoría y la traza de observabilidad correspondiente.
        """
        start_time = time.perf_counter()

        system_content = str(self.config.get("system_prompt", "")).format(
            project_id=settings.project_id, dataset_id=settings.dataset_id
        )

        messages = [
            SystemMessage(content=system_content),
            HumanMessage(
                content=f"User Intent: {user_query}\nGenerated SQL: {generated_sql}"
            ),
        ]

        raw_verdict = await self.model.ainvoke(messages)
        verdict = cast(ValidationVeredict, raw_verdict)

        duration = time.perf_counter() - start_time

        trace = TraceStep(
            name="SQL Audit Node",
            duration=duration,
            details=verdict.model_dump(),
        )

        return verdict, trace
