"""
Módulo de configuración central del sistema.

Gestiona la carga, validación e inmutabilidad de las variables de entorno
requeridas para la ejecución de la aplicación, utilizando Pydantic Settings.
Implementa el principio fail-fast para dependencias críticas.
"""

import logging
from pathlib import Path
from typing import Final

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR: Final[Path] = Path(__file__).resolve().parent.parent

logger = logging.getLogger(__name__)


class EmptyEnvironmentVariableError(ValueError):
    """
    Excepción lanzada cuando una variable de entorno requerida está vacía.

    Asegura que las dependencias críticas no solo estén presentes en el
    entorno, sino que contengan valores válidos y no vacíos.
    """

    def __init__(self) -> None:
        super().__init__(
            "Este campo es obligatorio y no puede estar vacío en el entorno."
        )


class Settings(BaseSettings):
    """
    Configuración central del sistema validada mediante Pydantic.

    Diseñada bajo principios de inmutabilidad (frozen) y fail-fast.
    Asegura que las dependencias críticas estén presentes y validadas
    antes del inicio de la aplicación.

    Attributes:
        google_api_key (str): Clave de API para autenticación en servicios de Google (Gemini).
        project_id (str): Identificador del proyecto en Google Cloud Platform.
        dataset_id (str): Nombre del dataset en BigQuery (por defecto 'mibici_gdl').
        gemini_model (str): Nombre del modelo LLM a utilizar (por defecto 'gemini-2.5-flash').
        gemini_temperature (float): Grado de creatividad del modelo (rango 0.0 - 2.0).
    """

    google_api_key: str = Field(
        default="", validation_alias="GOOGLE_API_KEY", repr=False, validate_default=True
    )
    project_id: str = Field(
        default="", validation_alias="PROJECT_ID", validate_default=True
    )
    dataset_id: str = Field(default="mibici_gdl", validation_alias="DATASET_ID")

    @field_validator("google_api_key", "project_id")
    @classmethod
    def check_not_empty(cls, v: str) -> str:
        """
        Valida que el valor proporcionado no sea una cadena vacía o de solo espacios.

        Args:
            v: Valor de la variable de entorno extraída por Pydantic.

        Returns:
            str: La cadena original validada.

        Raises:
            EmptyEnvironmentVariableError: Si la cadena resultante está vacía o es espacio en blanco.
        """
        if not v.strip():
            raise EmptyEnvironmentVariableError()
        return v

    gemini_model: str = Field(
        default="gemini-2.5-flash", validation_alias="GEMINI_MODEL"
    )
    gemini_temperature: float = Field(
        default=0.0,
        validation_alias="GEMINI_TEMPERATURE",
        ge=0.0,
        le=2.0,
    )

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )


try:
    settings = Settings()
    logger.debug("Configuración de sistema cargada exitosamente.")
except Exception as e:
    logger.critical(f"Fallo crítico durante la inicialización de la configuración: {e}")
    raise
