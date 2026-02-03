import logging
import re
from typing import Any

from google.cloud import bigquery

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class QueryResult(BaseModel):
    data: list[list[Any]] = Field(default_factory=list)
    columns: list[str] = Field(default_factory=list)
    error: str | None = None


class BigQueryManager:
    _client: bigquery.Client | None = None

    @classmethod
    def get_client(cls) -> bigquery.Client:
        if cls._client is None:
            cls._client = bigquery.Client()
        return cls._client


def bq_executor(sql_query: str) -> QueryResult:
    """Limpia y ejecuta la consulta en GCP."""
    client = BigQueryManager.get_client()

    # Extrae solo el bloque SELECT por si el LLM incluye explicaciones
    match = re.search(r"(SELECT\s.*)", sql_query, re.IGNORECASE | re.DOTALL)
    clean_query = (
        match.group(1).replace("```sql", "").replace("```", "").strip()
        if match
        else sql_query.strip()
    )

    try:
        query_job = client.query(clean_query)
        results = query_job.result(timeout=30)
        return QueryResult(
            data=[list(row.values()) for row in results],
            columns=[field.name for field in results.schema],
        )
    except Exception as e:
        return QueryResult(error=f"Error en ejecución: {str(e)}")
