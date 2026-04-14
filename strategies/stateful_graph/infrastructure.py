"""
BigQuery Infrastructure Provider Module.

Manages the lifecycle and connection state of the Google BigQuery client.
Implements a module-level singleton pattern to ensure connection reuse
across multiple agent tool invocations, optimizing latency and resource usage.
"""

from google.cloud import bigquery

from core.config import settings


class BigQueryProvider:
    """
    Infrastructure provider for Google BigQuery.

    Manages the client lifecycle using a module-level Singleton pattern,
    avoiding the use of explicit 'global' statements while ensuring that
    authentication and connection state are established only once per session.
    """

    def __init__(self) -> None:
        """Initializes the provider without instantiating the client immediately (lazy loading)."""
        self._client: bigquery.Client | None = None

    def get_client(self) -> bigquery.Client:
        """
        Retrieves the unique, lazy-loaded BigQuery client instance for the current session.

        Returns:
            The active `bigquery.Client` instance configured for the target project.
        """
        if self._client is None:
            # SoC: Configuration is extracted centrally from core.config
            self._client = bigquery.Client(project=settings.project_id)
        return self._client


# Module-level singleton instance for shared usage across tools.
bq_provider = BigQueryProvider()
