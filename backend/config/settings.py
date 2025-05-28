# backend/config/settings.py

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field
import os
import logging

# ─────────────────────────────────────────────────────────────────────────────
# ✅ Cargar .env automáticamente
# ─────────────────────────────────────────────────────────────────────────────
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    logging.warning(f"⚠️  Archivo .env no encontrado en: {dotenv_path}")


# ─────────────────────────────────────────────────────────────────────────────
# 📦 Configuración general del sistema Cuentix
# ─────────────────────────────────────────────────────────────────────────────
class Settings(BaseSettings):
    # 🔐 Claves de API
    DEEPSEEK_API_KEY: str = Field(..., env="DEEPSEEK_API_KEY")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_PROJECT_ID: str = Field(..., env="OPENAI_PROJECT_ID")
    ELEVENLABS_API_KEY: str = Field(..., env="ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID: str = Field("EXAVITQu4vr4xnSDxMaL", env="ELEVENLABS_VOICE_ID")

    # 🗣️ Motor de texto a voz y modelo de Whisper
    TTS_ENGINE: str = Field("gtts", env="TTS_ENGINE")
    WHISPER_MODEL_SIZE: str = Field("base", env="WHISPER_MODEL_SIZE")

    # 📁 Rutas de carpetas (sobrescribibles desde .env)
    AUDIO_DIR: str = Field(default="assets/audio", env="AUDIO_DIR")
    IMAGES_DIR: str = Field(default="assets/images", env="IMAGES_DIR")
    VIDEO_DIR: str = Field(default="assets/videos", env="VIDEO_DIR")
    SUBTITLES_DIR: str = Field(default="assets/subtitles", env="SUBTITLES_DIR")
    TEXT_DIR: str = Field(default="assets/text", env="TEXT_DIR")

    class Config:
        extra = "forbid"
        populate_by_name = True

    def crear_carpetas(self):
        """
        Crea automáticamente las carpetas base definidas en la configuración.
        Se llama una sola vez al importar el archivo.
        """
        for ruta in [
            self.AUDIO_DIR,
            self.IMAGES_DIR,
            self.VIDEO_DIR,
            self.SUBTITLES_DIR,
            self.TEXT_DIR
        ]:
            os.makedirs(ruta, exist_ok=True)
            logging.debug(f"📁 Carpeta verificada: {ruta}")


# Instancia compartida
settings = Settings()
settings.crear_carpetas()
