"""
Proveedor principal de modelos de lenguaje (LLM).

Gestiona la inicialización, configuración y ciclo de vida de los modelos
generativos de Google (Gemini) a través de la integración con LangChain.
Implementa un mecanismo de caché en memoria para optimizar la reutilización
de instancias y reducir la sobrecarga de conexiones.
"""

import logging

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

from core.config import settings

logger = logging.getLogger(__name__)


class MissingAPIKeyError(ValueError):
    """Excepción lanzada cuando la API Key de Google no está configurada."""

    def __init__(self) -> None:
        super().__init__(
            "Google API Key es requerida. Verifica tu archivo .env o variables de entorno."
        )


class LLMProvider:
    """
    Clase proveedora para la configuración e instanciación de modelos Gemini.

    Centraliza la inyección de dependencias (clave API, modelo por defecto,
    temperatura) y aplica configuraciones de seguridad. Mantiene un registro
    interno (caché) de las instancias creadas para garantizar eficiencia en
    entornos de ejecución repetitiva (como flujos agénticos).

    Attributes:
        api_key (str): Clave de autenticación para la API de Google.
        default_model (str): Nombre del modelo Gemini a usar por defecto.
        temperature (float): Nivel de creatividad/aleatoriedad por defecto.
        max_retries (int): Cantidad máxima de reintentos ante fallos de red (default: 3).
        timeout (int): Tiempo máximo de espera en segundos por petición (default: 120).
    """

    def __init__(
        self,
        api_key: str | None = None,
        default_model: str | None = None,
        default_temperature: float | None = None,
    ) -> None:
        """
        Inicializa el proveedor de LLM, aplica configuraciones de resiliencia
        y valida las credenciales requeridas.

        Args:
            api_key: Clave API de Google. Si es None, recae en settings.google_api_key.
            default_model: Modelo a utilizar. Si es None, recae en settings.gemini_model.
            default_temperature: Temperatura a utilizar. Si es None, recae en settings.gemini_temperature.

        Raises:
            MissingAPIKeyError: Si no se resuelve ninguna clave API válida.
        """
        self.api_key = api_key or settings.google_api_key
        self.default_model = default_model or settings.gemini_model
        self.temperature = (
            default_temperature
            if default_temperature is not None
            else settings.gemini_temperature
        )

        self.max_retries = 3
        self.timeout = 120
        self._cache: dict[tuple[str, float], ChatGoogleGenerativeAI] = {}

        if not self.api_key:
            logger.critical("Fallo crítico: No se proporcionó Google API Key.")
            raise MissingAPIKeyError()

    def get_llm(
        self, model_name: str | None = None, temperature: float | None = None
    ) -> ChatGoogleGenerativeAI:
        """
        Obtiene o crea una instancia configurada de Gemini (ChatGoogleGenerativeAI).

        Implementa un patrón de memorización (caché por instancia) basado en la
        combinación de modelo y temperatura para evitar la instanciación redundante.
        Utiliza resolución local de variables para asegurar la estrictez de tipos.

        Args:
            model_name: Nombre del modelo a utilizar. Si es None, usa el valor por defecto.
            temperature: Nivel de temperatura/creatividad. Si es None, usa el valor por defecto.

        Returns:
            ChatGoogleGenerativeAI: Instancia del modelo recuperada o recién creada.
        """
        target_model: str = model_name if model_name is not None else self.default_model
        target_temp = temperature if temperature is not None else self.temperature

        cache_key = (target_model, target_temp)
        if cache_key not in self._cache:
            self._cache[cache_key] = ChatGoogleGenerativeAI(
                model=target_model,
                temperature=target_temp,
                google_api_key=self.api_key,
                max_retries=self.max_retries,
                timeout=self.timeout,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                },
            )
        return self._cache[cache_key]


provider: LLMProvider = LLMProvider()
