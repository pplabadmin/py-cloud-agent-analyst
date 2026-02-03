from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from engines.linear.prompts import INVENTORY_PROMPT, ROUTER_PROMPT, SALES_PROMPT


class LLMManager:
    _instance: ChatGoogleGenerativeAI | None = None

    @classmethod
    def get_model(cls) -> ChatGoogleGenerativeAI:
        if cls._instance is None:
            cls._instance = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash", temperature=0
            )
        return cls._instance


def get_sql_and_intent(query: str) -> tuple[str, str]:
    """Genera el SQL y detecta la intención para inspección en UI."""
    llm = LLMManager.get_model()
    # Ruteo semántico
    intent = (
        (ROUTER_PROMPT | llm | StrOutputParser())
        .invoke({"input": query})
        .strip()
        .upper()
    )

    prompt = INVENTORY_PROMPT if intent == "INVENTORY" else SALES_PROMPT
    sql = (prompt | llm | StrOutputParser()).invoke({"input": query})
    return sql, intent
