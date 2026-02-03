import logging
import sys

from engines.linear.pipeline import full_pipeline

logging.getLogger("google").setLevel(logging.WARNING)
logging.getLogger("langchain").setLevel(logging.WARNING)

logger = logging.getLogger("main")


def main():
    logger.info("Iniciando Sistema Experto MiBici GDL")

    # Si hay argumentos en la terminal, úsalos; si no, usa la hardcoded
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = "¿Cuántos viajes hubo en 2014 vs 2026?"

    logger.info("Pregunta a procesar: %s", question)

    try:
        # El flujo interno ya genera logs de lo que está pasando
        answer = full_pipeline.invoke(question)
        logger.info("RESPUESTA FINAL:\n%s\n", answer)
    except Exception:  # pylint: disable=broad-except
        logger.exception("Error fatal en el pipeline principal")


if __name__ == "__main__":
    main()
