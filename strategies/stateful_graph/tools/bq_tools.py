"""
BigQuery Execution Tools Module.

Provides specialized tools for the AI agent to interact directly with Google BigQuery.
Enforces stateful security and execution guardrails (e.g., ensuring prerequisite
skills are loaded before allowing query execution) to prevent hallucinated or
unsafe SQL operations.
"""

import logging
from typing import Any

from langchain.tools import ToolRuntime, tool

from strategies.stateful_graph.infrastructure import bq_provider
from strategies.stateful_graph.state import MiBiciState

logger = logging.getLogger(__name__)


@tool
def execute_query(
    sql: str, runtime: ToolRuntime[None, MiBiciState]
) -> list[dict[str, Any]]:
    """
    Executes a generated SQL SELECT query on BigQuery and returns the results.

    This tool acts as a safeguard. It enforces the "Progressive Disclosure" pattern
    by requiring the agent to have previously loaded the 'sql_query_expert' skill.
    This ensures the agent is aware of schema constraints and SQL dialect rules
    before attempting execution.

    Args:
        sql: The BigQuery-compatible SQL query string to execute.
        runtime: The LangChain tool runtime injected automatically, providing
            access to the current state of the graph.

    Returns:
        A list of dictionaries representing the rows returned by the query,
        or a standardized error dictionary if validation or execution fails.
    """
    # 1. Sincronización del nombre de la habilidad
    skills_active = runtime.state.get("skills_loaded", [])

    if "sql_query_expert" not in skills_active:  # Nombre sincronizado con registry.py
        return [
            {
                "error": "Permiso denegado",
                "detalle": "Debes cargar la habilidad 'sql_query_expert' para conocer el esquema.",
            }
        ]

    # 2. Ejecución física
    client = bq_provider.get_client()
    try:
        query_job = client.query(sql)
        results = query_job.result()
        return [dict(row) for row in results]
    except Exception as e:
        logger.exception(f"BigQuery execution failed for query:\n{sql}")
        return [
            {
                "error": "Fallo técnico en la infraestructura de datos.",
                "detalle": str(e),
            }
        ]
