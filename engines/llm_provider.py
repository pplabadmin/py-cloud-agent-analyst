import os

from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

load_dotenv()


class MissingEnvironmentVariableError(ValueError):
    def __init__(self, variable_name: str):
        super().__init__(f"La variable de entorno {variable_name} no está configurada.")


class LLMProvider:
    """
    Maneja la instancia de Gemini de forma atómica.
    Optimizado para determinismo en análisis de datos.
    """

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise MissingEnvironmentVariableError("GOOGLE_API_KEY")

        self.model_name = os.getenv("GEMINI_MODEL")
        if not self.model_name:
            raise MissingEnvironmentVariableError("GEMINI_MODEL")

        self.temperature = os.getenv("GEMINI_TEMPERATURE")
        if not self.temperature:
            raise MissingEnvironmentVariableError("GEMINI_TEMPERATURE")
        self.temperature = float(self.temperature)

    def get_llm(self):
        """
        Retorna la instancia del chat model configurada para el pipeline.
        """
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            google_api_key=self.api_key,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            },
        )


provider = LLMProvider()
gemini_llm = provider.get_llm()
