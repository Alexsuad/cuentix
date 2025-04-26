# core/processors/audio_generator_openai.py

import os
import openai
from config.settings import settings          # Clave API desde .env
from utils.logger import get_logger           # Logger personalizado

# Creamos un logger específico para este módulo
logger = get_logger(__name__)

class OpenAITTS:
    """
    Generador de audio alternativo usando la nueva API de OpenAI (modelo tts-1).
    Ideal para pruebas o prototipos, con voces realistas en español.
    """

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.voice = "alloy"  # Puedes probar: alloy, echo, fable, onyx, nova, shimmer
        self.output_dir = "assets/audio"
        os.makedirs(self.output_dir, exist_ok=True)
        openai.api_key = self.api_key

    def generate_audio(self, texto: str, nombre_archivo: str = "openai_audio.mp3") -> str:
        """
        Convierte texto en audio y guarda el resultado como .mp3 usando OpenAI TTS.

        Parámetros:
        - texto (str): Texto a convertir.
        - nombre_archivo (str): Nombre del archivo de salida.

        Retorna:
        - str: Ruta del archivo generado.
        """
        try:
            logger.info("Generando audio con OpenAI TTS...")

            response = openai.Audio.create(
                model="tts-1",        # También puedes usar "tts-1-hd"
                input=texto,
                voice=self.voice
            )

            ruta_salida = os.path.join(self.output_dir, nombre_archivo)
            with open(ruta_salida, "wb") as f:
                f.write(response["data"])

            logger.info(f"Audio guardado en: {ruta_salida}")
            return ruta_salida

        except Exception as e:
            logger.error(f"Error al generar audio con OpenAI: {str(e)}")
            return ""
