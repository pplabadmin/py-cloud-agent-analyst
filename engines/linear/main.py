import logging
import sys

from dotenv import load_dotenv

from engines.linear.pipeline import run_linear_engine

# Configuración de logging profesional
# Usamos el stream de stdout para que Cloud Run capture los logs correctamente
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

MIN_REQUIRED_ARGS = 2


def main():
    """Ejecuta el benchmark lineal con validación estricta de entrada."""
    load_dotenv()

    # 1. Validación de Input: Error explícito si no hay entrada
    # En un entorno profesional, no 'suponemos' una pregunta si el CLI es la interfaz
    if len(sys.argv) < MIN_REQUIRED_ARGS:
        logger.error("Falta el argumento de entrada. Uso: python main.py '<pregunta>'")
        sys.exit(1)  # Salida con error para integración con scripts/pipelines

    question = " ".join(sys.argv[1:])
    logger.info("Iniciando benchmark lineal para la consulta: '%s'", question)

    try:
        # 2. Ejecución del motor
        result = run_linear_engine(question)

        # 3. Manejo de errores de negocio
        if result.error:
            logger.error("El motor lineal devolvió un error: %s", result.error)
            sys.exit(1)

        # 4. Reporte de resultados vía Logging
        # Evitamos f-strings en logs para mantener el 'lazy formatting'
        logger.info("Ejecución exitosa.")
        logger.info("Columnas detectadas: %s", result.columns)

        # Logueamos solo una muestra para evitar saturar el buffer de logs en GCP
        sample_data = result.data[:3]
        logger.info("Muestra de datos (3 filas): %s", sample_data)

        logger.warning(
            "Nota: El sistema lineal es ciego a estados operativos externos."
        )

    except Exception as e:  # pylint: disable=broad-exception-caught
        # Captura de errores de infraestructura (conexión GCP, etc.)
        logger.critical("Fallo crítico en la infraestructura del benchmark: %s", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
