"""
Módulo de observabilidad y logging centralizado.

Proporciona la configuración estándar de logging para toda la aplicación,
implementando un enfoque de doble salida: consola (mediante Rich para
formato avanzado) y archivo rotativo (para persistencia segura y eficiente
en entornos productivos).
"""

import logging
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler

from core.config import ROOT_DIR


def setup_logging(level: str | int = logging.INFO) -> None:
    """
    Configura el sistema central de observabilidad y logging de la aplicación.

    Establece un doble canal de salida:
    1. Consola (Rich): Formato amigable y legible para el desarrollador con soporte markup.
    2. Archivo (Rotating): Rotación automática para evitar saturación de disco,
       manteniendo un historial manejable para operaciones y auditoría.

    Adicionalmente, esta función purga los handlers existentes para evitar logs
    duplicados y reduce la verbosidad de librerías de terceros (httpx, google,
    langchain) para minimizar el ruido en los registros.

    Args:
        level: Nivel base de severidad para el root logger. Puede ser una cadena
            de texto (ej. "INFO") o una constante de logging (ej. logging.INFO).
    """
    log_dir = ROOT_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "querymind.log"

    file_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    console_handler = RichHandler(rich_tracebacks=True, markup=True)
    root_logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8", delay=False
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("langchain").setLevel(logging.WARNING)

    logging.info(f"🚀 Sistema de observabilidad iniciado. Archivo: {log_file}")
