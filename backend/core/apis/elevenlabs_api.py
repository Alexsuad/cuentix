# core/apis/elevenlabs_api.py

# Este módulo se encarga de enviar texto a ElevenLabs para convertirlo en audio (TTS).
# Implementa manejo de errores, reintentos con tenacity y validación de claves.

import requests
import os
from config.settings import settings
from utils.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = get_logger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def convertir_texto_a_audio_elevenlabs(texto: str, nombre_archivo: str, voice_id: str = None) -> str:
    """
    Envía texto a la API de ElevenLabs y guarda el resultado como un archivo de audio MP3.

    Parámetros:
    - texto (str): El texto a convertir.
    - nombre_archivo (str): Nombre de salida del archivo.
    - voice_id (str): ID de la voz a utilizar. Si no se especifica, se toma del .env.

    Retorna:
    - str: Ruta del archivo de audio generado o cadena vacía si falla.
    """
    try:
        if voice_id is None:
            voice_id = settings.ELEVENLABS_VOICE_ID

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": settings.ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": texto,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.7
            }
        }

        logger.info("🎙️ Enviando texto a ElevenLabs para TTS...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        ruta_audio = os.path.join("assets/audio", nombre_archivo)
        os.makedirs(os.path.dirname(ruta_audio), exist_ok=True)

        with open(ruta_audio, "wb") as f:
            f.write(response.content)

        logger.info(f"✅ Audio generado correctamente en: {ruta_audio}")
        return ruta_audio

    except requests.HTTPError as e:
        if e.response.status_code == 429:
            logger.warning("⚠️ Límite de solicitudes a ElevenLabs excedido (429). Reintentando...")
        elif e.response.status_code == 401:
            logger.error("❌ Clave API inválida o no autorizada en ElevenLabs (401)")
        else:
            logger.error(f"❌ Error HTTP en ElevenLabs: {e.response.status_code}")
        raise
    except Exception as e:
        logger.error(f"❌ Error inesperado en ElevenLabs: {str(e)}")
        return ""
