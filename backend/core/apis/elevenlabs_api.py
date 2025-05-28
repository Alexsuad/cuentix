# core/apis/elevenlabs_api.py

# Este módulo convierte texto a voz usando la API de ElevenLabs.
# Requiere una clave API válida y una voz ID configurada.

from config.settings import settings
from utils.logger import get_logger
from elevenlabs.client import ElevenLabs

import os

logger = get_logger(__name__)

def convertir_texto_a_audio_elevenlabs(texto: str, ruta_salida: str) -> str:
    """
    Convierte texto a voz usando ElevenLabs API y guarda el audio como archivo MP3.

    Parámetros:
    - texto (str): Texto a convertir.
    - ruta_salida (str): Ruta completa donde guardar el archivo .mp3

    Retorna:
    - str: Ruta al archivo generado o "" si ocurre un error.
    """
    try:
        # Crear carpeta si no existe
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

        # Inicializar cliente ElevenLabs
        client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)

        logger.info("🎤 Enviando texto a ElevenLabs TTS...")

        audio = client.text_to_speech.convert(
            voice_id=settings.ELEVENLABS_VOICE_ID,
            text=texto,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100"
        )

        with open(ruta_salida, "wb") as f:
            f.write(audio)

        logger.info(f"✅ Audio generado con ElevenLabs en: {ruta_salida}")
        return ruta_salida

    except Exception as e:
        logger.error(f"❌ Error al generar audio con ElevenLabs: {e}")
        return ""
