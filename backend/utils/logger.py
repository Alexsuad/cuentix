# utils/logger.py
# Configuración centralizada del sistema de logging para Cuentix.
# Este módulo define un logger unificado con salida a archivo (con rotación) y consola.

import logging
from logging.handlers import RotatingFileHandler
import os

# Crear carpeta de logs si no existe
os.makedirs("logs", exist_ok=True)

# Ruta del archivo de log
log_path = os.path.join("logs", "app.log")

# Formato estándar para todos los logs
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Nivel por defecto (puede cambiarse a DEBUG en desarrollo)
DEFAULT_LEVEL = logging.INFO

def get_logger(nombre: str) -> logging.Logger:
    """
    Retorna un logger configurado con salida a archivo y consola.
    - Rota el archivo cuando supera 1 MB (mantiene 3 backups).
    """
    logger = logging.getLogger(nombre)
    logger.setLevel(DEFAULT_LEVEL)

    if not logger.handlers:
        # Handler para archivo con rotación
        file_handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)

    return logger
