"""
Contratos de datos para la lógica de validación y ejecución.

Este módulo define los esquemas Pydantic utilizados para estructurar y
validar los datos en los pasos intermedios de la cadena de evaluación,
tales como la auditoría de seguridad (Validator) y la ejecución física
de consultas (Connector).
"""

from typing import Any

from pydantic import BaseModel, Field


class ValidationVeredict(BaseModel):
    """
    Contrato de auditoría técnica para el paso de validación.

    Representa la evaluación estructurada producida por el nodo validador.
    Garantiza que la consulta generada cumpla con las políticas de seguridad
    (prevención de inyecciones) y que semánticamente responda a la solicitud del usuario.

    Attributes:
        is_safe (bool): Bandera que indica si la consulta es de solo lectura (segura).
        is_semantically_correct (bool): Bandera que indica si el SQL se alinea con la intención del usuario.
        feedback (str): Explicación técnica detallada del auditor justificando su decisión.
    """

    is_safe: bool = Field(
        ...,
        description="Indica si la consulta es segura (estrictamente sentencias SELECT).",
    )
    is_semantically_correct: bool = Field(
        ...,
        description="Indica si el SQL generado responde con precisión a la pregunta del usuario.",
    )
    feedback: str = Field(
        ...,
        description="Crítica técnica detallada del auditor justificando la aprobación o rechazo.",
    )


class ConnectorOutput(BaseModel):
    """
    Contrato de salida para la ejecución física en BigQuery.

    Estandariza la respuesta de la base de datos, encapsulando tanto el
    resultado exitoso (filas y métricas de rendimiento) como los posibles
    fallos de ejecución, para su posterior interpretación por el nodo final.

    Attributes:
        data (list[dict[str, Any]]): Lista de registros recuperados, donde cada diccionario representa una fila.
        row_count (int): Número total de filas devueltas por la consulta.
        execution_time (float): Tiempo total de ejecución de la consulta en la base de datos, en segundos.
        error (str | None): Mensaje de error detallado en caso de fallo, o None si la ejecución fue exitosa.
    """

    data: list[dict[str, Any]] = Field(
        default_factory=list, description="Dataset crudo recuperado de BigQuery."
    )
    row_count: int = Field(
        default=0, description="Total de filas recuperadas en la consulta."
    )
    execution_time: float = Field(
        default=0.0, description="Tiempo de ejecución de la consulta en segundos."
    )
    error: str | None = Field(
        default=None,
        description="Detalle del error devuelto por el motor de base de datos, si falló.",
    )
