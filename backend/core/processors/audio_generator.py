# ──────────────────────────────────────────────────────────────────────────────
# File: backend/core/processors/audio_generator.py
# Descripción: Gestiona la generación de audio desde texto, con soporte para
# múltiples motores (gTTS, OpenAI, ElevenLabs). Orquesta las llamadas a las APIs.
# ──────────────────────────────────────────────────────────────────────────────

import os
from pathlib import Path
from config.settings import settings
from utils.logger import get_logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import requests

logger = get_logger(__name__)

class AudioGenerator:
    def __init__(self, motor: str = "openai"):
        self.motor = motor.lower()
        self.logger = logger
        self.logger.info(f"🔈 AudioGenerator inicializado con motor: {self.motor}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.ConnectionError))
    )
    def _generate_audio_gtts(self, texto: str, ruta_salida: str) -> str:
        from gtts import gTTS
        self.logger.info("🎤 Enviando texto a gTTS...")
        tts = gTTS(text=texto, lang="es")
        tts.save(ruta_salida)
        self.logger.info(f"✅ Audio generado con gTTS en: {ruta_salida}")
        return ruta_salida

    def generate_audio(self, texto: str, ruta_salida: str) -> str:
        if not texto or not texto.strip():
            self.logger.warning("⚠️ Texto vacío recibido para generar audio.")
            return ""

        try:
            ruta_obj = Path(ruta_salida)
            ruta_obj.parent.mkdir(parents=True, exist_ok=True)

            # 🎙️ Motor principal
            if self.motor == "gtts":
                return self._generate_audio_gtts(texto, ruta_salida)

            elif self.motor == "openai":
                from core.apis.openai_tts_api import convertir_texto_a_audio_openai
                try:
                    return convertir_texto_a_audio_openai(texto, ruta_salida)
                except Exception as e:
                    self.logger.warning(f"⚠️ OpenAI TTS falló: {e}. Reintentando con gTTS...")
                    return self._generate_audio_gtts(texto, ruta_salida)

            elif self.motor == "elevenlabs":
                from core.apis.elevenlabs_api import convertir_texto_a_audio_elevenlabs
                try:
                    return convertir_texto_a_audio_elevenlabs(texto, ruta_salida)
                except Exception as e:
                    self.logger.warning(f"⚠️ ElevenLabs TTS falló: {e}. Reintentando con gTTS...")
                    return self._generate_audio_gtts(texto, ruta_salida)

            else:
                raise ValueError(f"Motor de TTS '{self.motor}' no soportado.")

        except Exception as e:
            self.logger.error(f"❌ Error inesperado al generar audio con motor '{self.motor}': {e}")
            return ""
