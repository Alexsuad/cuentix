# ──────────────────────────────────────────────────────────────
# File: backend/utils/paths.py
# Descripción: Función auxiliar para construir rutas absolutas
# dentro de las carpetas definidas en settings (audio, video, etc).
# ──────────────────────────────────────────────────────────────

import os
from config.settings import settings
from pathlib import Path

def new_asset_path(tipo: str, nombre_archivo: str) -> str:
    """
    Devuelve la ruta absoluta para guardar un archivo de tipo dado (audio, video, etc).

    Args:
        tipo (str): Subcarpeta dentro de assets. Ej: "audio", "images", "subtitles", "video".
        nombre_archivo (str): Nombre del archivo con extensión.

    Returns:
        str: Ruta absoluta combinada, lista para usar.
    """
    base_dir = {
        "audio": settings.AUDIO_DIR,
        "images": settings.IMAGES_DIR,
        "subtitles": settings.SUBTITLES_DIR,
        "videos": settings.VIDEOS_DIR,
    }.get(tipo)

    if not base_dir:
        raise ValueError(f"Tipo de asset desconocido: {tipo}")

    return str(Path(base_dir) / nombre_archivo)
