import logging

from google.cloud import bigquery

# Configuración básica de logging para la demo
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("core.tools")


class BigQueryTool:
    def __init__(self):
        self.client = bigquery.Client()

    def execute_query(self, sql: str) -> str:
        logger.info("Ejecutando SQL en BigQuery: %s", sql)
        try:
            query_job = self.client.query(sql)
            results = query_job.result()
            df = results.to_dataframe()

            if df.empty:
                logger.warning("La consulta no devolvió resultados.")
                return "No se encontraron datos."

            logger.info("Consulta exitosa. Filas recuperadas: %s", len(df))
            return df.to_string(index=False)
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Falla en ejecución de BigQuery: %s", e)
            return f"Error de infraestructura: {str(e)}"


bq_tool = BigQueryTool()
