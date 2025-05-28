# core/processors/audio_generator.py

# Módulo que gestiona la generación de audio desde texto, con soporte para múltiples motores (gTTS, OpenAI, ElevenLabs).

import os
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)

class AudioGenerator:
    def __init__(self, motor: str = "openai"):
        # Motor seleccionado (gtts, openai, elevenlabs)
        self.motor = motor.lower()
        self.logger = get_logger(__name__)
        self.logger.info(f"🔈 AudioGenerator inicializado con motor: {self.motor}")

    def generate_audio(self, texto: str, nombre_archivo: str) -> str:
        try:
            ruta = Path(nombre_archivo)
            ruta.parent.mkdir(parents=True, exist_ok=True)

            if self.motor == "gtts":
                from gtts import gTTS
                tts = gTTS(text=texto, lang="es")
                tts.save(nombre_archivo)
                return str(nombre_archivo)

            elif self.motor == "openai":
                from core.apis.openai_tts_api import convertir_texto_a_audio_openai
                return convertir_texto_a_audio_openai(texto, str(ruta))

            elif self.motor == "elevenlabs":
                from core.apis.elevenlabs_api import convertir_texto_a_audio_elevenlabs
                return convertir_texto_a_audio_elevenlabs(texto, os.path.basename(nombre_archivo))

            else:
                raise ValueError(f"Motor {self.motor} no soportado")

        except Exception as e:
            self.logger.error(f"❌ Error al generar audio con {self.motor}: {e}")
            return ""
