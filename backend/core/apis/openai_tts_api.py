# core/apis/openai_tts_api.py

# Este módulo convierte texto a voz usando la API de OpenAI Text-to-Speech (TTS).
# Implementa manejo de errores, reintentos con tenacity y control de tiempo de espera.

import requests
import os
from config.settings import settings
from utils.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = get_logger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def convertir_texto_a_audio_openai(texto: str, nombre_archivo: str, voz: str = "alloy") -> str:
    """
    Convierte texto a voz usando la API de OpenAI TTS y guarda el resultado como archivo .mp3.

    Parámetros:
    - texto (str): Texto a convertir en voz.
    - nombre_archivo (str): Nombre del archivo de salida.
    - voz (str): Voz seleccionada (alloy, echo, fable, onyx, nova, shimmer).

    Retorna:
    - str: Ruta al archivo generado o "" si ocurre un error.
    """
    ruta_audio = os.path.join("assets/audio", nombre_archivo)
    os.makedirs(os.path.dirname(ruta_audio), exist_ok=True)

    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
    }

    data = {
        "model": "tts-1",
        "input": texto,
        "voice": voz
    }

    try:
        logger.info("🎤 Enviando texto a OpenAI TTS...")
        response = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=data, timeout=30)
        response.raise_for_status()

        with open(ruta_audio, "wb") as f:
            f.write(response.content)

        logger.info(f"✅ Audio generado con OpenAI en: {ruta_audio}")
        return ruta_audio

    except requests.HTTPError as e:
        if e.response.status_code == 429:
            logger.warning("⚠️ Límite de tasa de OpenAI alcanzado (429). Reintentando...")
        elif e.response.status_code == 401:
            logger.error("❌ API Key inválida para OpenAI (401)")
        else:
            logger.error(f"❌ Error HTTP en OpenAI TTS: {e.response.status_code}")
        raise
    except Exception as e:
        logger.error(f"❌ Error inesperado al generar audio con OpenAI TTS: {e}")
        return ""
