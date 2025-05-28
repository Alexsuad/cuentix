# core/apis/openai_tts_api.py

import requests
import os
from config.settings import settings
from utils.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = get_logger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def convertir_texto_a_audio_openai(texto: str, ruta_salida: str, voz: str = "alloy") -> str:
    """
    Convierte texto a voz usando la API de OpenAI TTS y guarda el resultado como archivo .mp3.

    Parámetros:
    - texto (str): Texto a convertir en voz.
    - ruta_salida (str): Ruta completa donde guardar el archivo.
    - voz (str): Voz seleccionada (alloy, echo, fable, onyx, nova, shimmer).

    Retorna:
    - str: Ruta al archivo generado o "" si ocurre un error.
    """
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

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

        with open(ruta_salida, "wb") as f:
            f.write(response.content)

        logger.info(f"✅ Audio generado con OpenAI en: {ruta_salida}")
        return ruta_salida

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
