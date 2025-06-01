# ──────────────────────────────────────────────────────────────────────────────
# File: backend/core/processors/subtitles_utils.py
# Propósito: Utilidades para trabajar con subtítulos .srt en Cuentix.
# Convierte archivos .srt en listas JSON para uso en sincronización de video.
# ──────────────────────────────────────────────────────────────────────────────

import re
from utils.logger import get_logger
from typing import List, Dict
from pathlib import Path

logger = get_logger(__name__)

# --- Función Auxiliar: Conversión de tiempo SRT a segundos ---
def srt_time_to_seconds(srt_time: str) -> float:
    """
    Convierte un timestamp de formato SRT (ej. '00:01:02,500') a segundos.

    Args:
        srt_time (str): Tiempo en formato SRT.

    Returns:
        float: Tiempo en segundos (puede incluir decimales).
    """
    try:
        h, m, s_ms = srt_time.split(":")
        s, ms = s_ms.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    except Exception as e:
        logger.error(f"❌ Error al convertir tiempo SRT '{srt_time}': {e}")
        return 0.0

# --- Función Principal: Conversión de archivo .srt a JSON ---
def srt_to_json_simple(srt_path: str) -> List[Dict[str, float]]:
    """
    Lee un archivo .srt y lo transforma en una lista de subtítulos con tiempo y texto.

    Args:
        srt_path (str): Ruta al archivo .srt.

    Returns:
        list: Lista de dicts con claves 'start', 'end', 'text'. Retorna lista vacía si hay error.
    """
    subtitulos = []

    # Validación de lectura de archivo
    try:
        with open(srt_path, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        logger.error(f"❌ Archivo SRT no encontrado: {srt_path}")
        return []
    except Exception as e:
        logger.error(f"❌ Error al leer archivo SRT: {e}")
        return []

    # Separar por bloques (subtítulo por subtítulo)
    bloques = re.split(r"\n\s*\n", contenido.strip())

    for bloque in bloques:
        try:
            lineas = bloque.strip().split("\n")
            if len(lineas) >= 3:
                tiempos = lineas[1].strip()
                texto = " ".join(lineas[2:]).strip()

                match = re.match(
                    r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})",
                    tiempos
                )

                if match:
                    start = srt_time_to_seconds(match.group(1))
                    end = srt_time_to_seconds(match.group(2))
                    subtitulos.append({"start": start, "end": end, "text": texto})
                else:
                    logger.warning(f"⚠️ Tiempo mal formateado en bloque:\n{tiempos}")

        except Exception as e:
            logger.warning(
                f"⚠️ Bloque ignorado por error de parsing: {e}\nContenido del bloque:\n{bloque}\n"
            )
            continue

    return subtitulos
