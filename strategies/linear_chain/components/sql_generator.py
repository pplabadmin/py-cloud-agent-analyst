"""
Componente Arquitecto de Datos para la cadena de evaluación.

Este módulo define el nodo responsable de traducir intenciones de usuario
en lenguaje natural a consultas SQL de BigQuery optimizadas y seguras,
garantizando un contrato de salida estricto mediante Pydantic.
"""

import time
from pathlib import Path
from typing import Any, cast

import yaml
from langchain_core.messages import HumanMessage, SystemMessage

from core.config import settings
from core.providers import LLMProvider
from schema import TraceStep
from strategies.linear_chain.schemas.architect import SQLOutput


class ArchitectNode:
    """
    Nodo responsable de la generación de SQL con tipado estricto.

    Utiliza un modelo de lenguaje configurado para devolver respuestas
    estructuradas (JSON) que cumplen con el esquema SQLOutput. Carga su
    contexto y reglas de negocio desde un archivo de configuración YAML.

    Attributes:
        llm: Instancia del modelo de lenguaje con salida estructurada.
        prompt_path (Path): Ruta absoluta al archivo YAML de prompts.
        config (dict[str, Any]): Configuración y prompts cargados en memoria.
    """

    def __init__(self, provider: LLMProvider) -> None:
        current_file = Path(__file__).resolve()
        self.prompt_path = current_file.parent.parent / "prompts" / "architect.yaml"

        self.llm = provider.get_llm().with_structured_output(SQLOutput)

        with self.prompt_path.open(encoding="utf-8") as f:
            self.config = cast(dict[str, Any], yaml.safe_load(f))

    async def generate_sql(self, user_query: str) -> tuple[SQLOutput, TraceStep]:
        """
        Genera una consulta SQL a partir de la intención del usuario.

        Formatea el prompt del sistema con la configuración actual del entorno
        (proyecto y dataset), inyecta los ejemplos few-shot si existen,
        e invoca al LLM asíncronamente empaquetando el resultado.

        Args:
            user_query: Pregunta o instrucción del usuario en lenguaje natural.

        Returns:
            tuple[SQLOutput, TraceStep]: Tupla que contiene la salida estructurada
                (SQL validado, explicación, confianza) y la traza de observabilidad.
        """
        start_time = time.perf_counter()

        raw_system_prompt = str(self.config.get("system_prompt", ""))
        few_shots = self.config.get("few_shot_examples", [])

        if few_shots:
            raw_system_prompt += "\n\nFew-Shot Examples:\n"
            for ex in few_shots:
                raw_system_prompt += f"- User Intent: {ex.get('user_query')}\n  SQL: {ex.get('sql_logic')}\n"

        system_content = raw_system_prompt.format(
            project_id=settings.project_id, dataset_id=settings.dataset_id
        )

        messages = [
            SystemMessage(content=system_content),
            HumanMessage(content=user_query),
        ]

        response = await self.llm.ainvoke(messages)
        result = cast(SQLOutput, response)

        duration = time.perf_counter() - start_time

        trace = TraceStep(
            name="Architect SQL Generation",
            duration=duration,
            details={
                "sql": result.sql,
                "confidence": result.confidence_score,
                "explanation": result.explanation,
            },
        )

        return result, trace
