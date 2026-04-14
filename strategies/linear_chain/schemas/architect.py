"""
Define el contrato de datos para la salida estructurada del nodo Arquitecto.

Este módulo contiene el modelo Pydantic que LangChain utiliza para parsear
y validar la salida JSON del LLM cuando este genera consultas SQL.
"""

from pydantic import BaseModel, Field


class SQLOutput(BaseModel):
    """
    Representa la salida validada y estructurada del LLM para la generación de SQL.

    Este modelo actúa como un contrato de datos que asegura que la respuesta del
    LLM contenga una consulta SQL válida, una explicación de su lógica y un
    puntaje de confianza. Facilita una integración segura y predecible
    en los siguientes pasos de la cadena de ejecución.

    Attributes:
        sql (str): La consulta SQL de BigQuery completa, optimizada y lista para ejecutar.
        explanation (str): Una breve explicación técnica de la lógica SQL aplicada,
                           útil para la trazabilidad y la interpretación por otros nodos.
        confidence_score (float): Un puntaje entre 0.0 y 1.0 que indica la confianza
                                  del LLM en la precisión y correctitud de la consulta generada.
    """

    sql: str = Field(
        ..., description="La consulta SQL de BigQuery completa y optimizada."
    )
    explanation: str = Field(
        ..., description="Breve explicación técnica de la lógica aplicada."
    )
    confidence_score: float = Field(
        ...,
        description="Nivel de confianza en la precisión del SQL (0.0 a 1.0).",
        ge=0.0,
        le=1.0,
    )
