"""
Componente de Infraestructura: Conector de BigQuery.

Este módulo gestiona la conexión y ejecución segura de consultas SQL
en Google BigQuery. Implementa adaptadores para no bloquear el bucle de
eventos asíncrono durante operaciones de I/O de red pesadas.
"""

import asyncio
import logging
import time
from typing import Any

from google.cloud import bigquery

from core.config import settings
from schema import TraceStep
from strategies.linear_chain.schemas.logic import ConnectorOutput

logger = logging.getLogger(__name__)


class BQConnector:
    """
    Nodo responsable de la ejecución física de consultas en BigQuery.

    Maneja el ciclo de vida del cliente de GCP y asegura que las llamadas
    síncronas de la API de Google no bloqueen el bucle de eventos de la aplicación.

    Attributes:
        client: Cliente oficial de BigQuery para la interacción con GCP.
    """

    def __init__(self, client: bigquery.Client | None = None):
        self.client = client or bigquery.Client(project=settings.project_id)

    def _run_sync_query(self, sql: str) -> list[dict[str, Any]]:
        """Ejecuta la consulta de forma síncrona. Diseñado para correr en un thread."""
        query_job = self.client.query(sql)
        results = query_job.result()
        return [dict(row) for row in results]

    async def execute(self, sql: str) -> tuple[ConnectorOutput, TraceStep]:
        """
        Ejecuta una consulta SQL en BigQuery de forma asíncrona.

        Delega la carga de trabajo bloqueante (I/O) a un hilo secundario
        para mantener la reactividad de la aplicación.

        Args:
            sql: La consulta SQL cruda a ejecutar.

        Returns:
            tuple[ConnectorOutput, TraceStep]: Contrato de salida con los datos o
                el error resultante, junto a la traza de observabilidad.
        """
        start_time = time.perf_counter()

        try:
            data = await asyncio.to_thread(self._run_sync_query, sql)

            duration = time.perf_counter() - start_time
            output = ConnectorOutput(
                data=data, row_count=len(data), execution_time=duration
            )

            status = "success"
        except Exception as e:
            logger.exception("Fallo en la ejecución física contra BigQuery.")
            duration = time.perf_counter() - start_time
            output = ConnectorOutput(error=str(e), execution_time=duration)
            status = "error"

        trace = TraceStep(
            name="BigQuery Infrastructure",
            duration=duration,
            details={
                "status": status,
                "row_count": output.row_count,
                "error": output.error,
            },
        )

        return output, trace
