import logging
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from core.tools import bq_tool
from engines.linear.prompts import INSIGHTS_PROMPT, SQL_GENERATOR_PROMPT
from engines.llm_provider import gemini_llm

logger = logging.getLogger("engines.linear.pipeline")


class SecurityScanError(ValueError):
    def __init__(self):
        super().__init__("Consulta bloqueada por seguridad.")


def sql_linter_node(sql_query: str) -> str:
    logger.debug("Iniciando validación de SQL (Linter)...")
    forbidden_pattern = r"(?i)\b(DROP|DELETE|UPDATE|TRUNCATE|INSERT)\b"
    clean_query = sql_query.replace("```sql", "").replace("```", "").strip()

    if re.search(forbidden_pattern, clean_query):
        logger.critical("Intento de inyección o comando prohibido: %s", clean_query)
        raise SecurityScanError()

    logger.info("SQL validado exitosamente.")
    return clean_query


# Definición del Pipeline (Grafo Lineal)
sql_chain = (
    {"pregunta": RunnablePassthrough()}
    | SQL_GENERATOR_PROMPT
    | gemini_llm
    | StrOutputParser()
    | sql_linter_node
)

full_pipeline = (
    {
        "datos_crudos": sql_chain | bq_tool.execute_query,
        "pregunta": RunnablePassthrough(),
    }
    | INSIGHTS_PROMPT
    | gemini_llm
    | StrOutputParser()
)
