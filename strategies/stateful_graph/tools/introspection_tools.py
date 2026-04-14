"""
BigQuery Introspection Tools Module.

Provides tools for the AI agent to dynamically explore the database schema.
These tools allow the agent to discover available tables and their detailed
column structures, reducing hallucination by relying on live metadata rather
than assumed schemas.
"""

import logging

from langchain.tools import tool

from core.config import settings
from strategies.stateful_graph.infrastructure import bq_provider

logger = logging.getLogger(__name__)


@tool
def list_dataset_tables() -> list[str]:
    """
    Lists all available tables within the configured BigQuery dataset.

    This tool enables the agent to discover available entities in the database
    before attempting to query them.

    Returns:
        A list of table IDs (strings) present in the dataset, or a list
        containing an error message if the introspection fails.
    """
    client = bq_provider.get_client()
    dataset_ref = client.dataset(settings.dataset_id)

    try:
        tables = client.list_tables(dataset_ref)
        return [table.table_id for table in tables]
    except Exception as e:
        logger.exception("Fallo crítico al listar tablas del dataset.")
        return [f"error: Fallo de introspección de catálogo. Detalle: {str(e)}"]


@tool
def get_table_schema(table_id: str) -> list[dict[str, str]]:
    """
    Retrieves the exact schema (columns and data types) for a specific table.

    Crucial for the agent to construct syntactically correct SQL queries,
    ensuring it uses the correct column names and respects data types.

    Args:
        table_id: The ID of the table to inspect (e.g., 'trips' or 'stations').

    Returns:
        A list of dictionaries, where each dictionary represents a column
        with 'column' (name) and 'type' keys. Returns an error dictionary
        if the table cannot be found or accessed.
    """
    client = bq_provider.get_client()
    table_ref = client.dataset(settings.dataset_id).table(table_id)

    try:
        table = client.get_table(table_ref)
        return [
            {"column": field.name, "type": field.field_type} for field in table.schema
        ]
    except Exception as e:
        logger.exception(f"No se pudo recuperar el esquema para la tabla: {table_id}")
        return [{"error": f"Esquema de '{table_id}' no disponible.", "detalle": str(e)}]
