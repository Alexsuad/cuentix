# ──────────────────────────────────────────────────────────────────────────────
# File: backend/config/settings.py
# Descripción: Configuración general del sistema Cuentix, cargada desde .env.
# Define claves de API, rutas de assets y otros parámetros configurables.
# ──────────────────────────────────────────────────────────────────────────────

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field
import os
import logging
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# ✅ Cargar .env automáticamente al importar este módulo
# ─────────────────────────────────────────────────────────────────────────────
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    logging.warning(f"⚠️  Archivo .env no encontrado en: {dotenv_path}. Las variables de entorno deben estar configuradas en el sistema.")

# ─────────────────────────────────────────────────────────────────────────────
# 📁 Definir rutas base del proyecto (constantes, fuera de la clase Settings)
# ─────────────────────────────────────────────────────────────────────────────
BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
PROMPT_TEMPLATE_PATH = PROJECT_ROOT / "assets" / "prompt_templates" / "prompt_base.txt"

# ─────────────────────────────────────────────────────────────────────────────
# 📦 Configuración general del sistema Cuentix (cargada desde .env)
# ─────────────────────────────────────────────────────────────────────────────
class Settings(BaseSettings):
    # 🔐 Claves de API
    DEEPSEEK_API_KEY: str = Field(..., env="DEEPSEEK_API_KEY")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_PROJECT_ID: str = Field(..., env="OPENAI_PROJECT_ID")
    ELEVENLABS_API_KEY: str = Field(..., env="ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID: str = Field("EXAVITQu4vr4xnSDxMaL", env="ELEVENLABS_VOICE_ID")

    # 🔐 Google Cloud (opcional)
    GOOGLE_CLOUD_PROJECT_ID: Optional[str] = Field(None, env="GOOGLE_CLOUD_PROJECT_ID")
    GOOGLE_CLOUD_REGION: str = Field("us-central1", env="GOOGLE_CLOUD_REGION")

    # 🗣️ Motores de IA
    TTS_ENGINE: str = Field("gtts", env="TTS_ENGINE")
    WHISPER_MODEL_SIZE: str = Field("base", env="WHISPER_MODEL_SIZE")

    # 🌐 API Base (soporte para DeepSeek)
    OPENAI_API_BASE: str = Field(default="https://api.openai.com/v1", env="OPENAI_API_BASE")

    # 📁 Rutas relativas (desde backend/) configurables por .env
    AUDIO_DIR: str = Field(default="assets/audio", env="AUDIO_DIR")
    IMAGES_DIR: str = Field(default="assets/images", env="IMAGES_DIR")
    VIDEOS_DIR: str = Field(default="assets/videos", env="VIDEOS_DIR")
    SUBTITLES_DIR: str = Field(default="assets/subtitles", env="SUBTITLES_DIR")
    TEXT_DIR: str = Field(default="assets/text", env="TEXT_DIR")

    # 📁 Rutas absolutas del proyecto (para acceso directo desde settings)
    BACKEND_DIR: Path = BACKEND_DIR
    PROJECT_ROOT: Path = PROJECT_ROOT
    PROMPT_TEMPLATE_PATH: Path = PROMPT_TEMPLATE_PATH

    class Config:
        extra = "forbid"
        populate_by_name = True

# Instancia compartida
settings = Settings()

# Crear directorios de assets si no existen
try:
    os.makedirs(settings.BACKEND_DIR / settings.AUDIO_DIR, exist_ok=True)
    os.makedirs(settings.BACKEND_DIR / settings.IMAGES_DIR, exist_ok=True)
    os.makedirs(settings.BACKEND_DIR / settings.VIDEOS_DIR, exist_ok=True)
    os.makedirs(settings.BACKEND_DIR / settings.SUBTITLES_DIR, exist_ok=True)
    os.makedirs(settings.BACKEND_DIR / settings.TEXT_DIR, exist_ok=True)
    logging.info("✅ Directorios de assets verificados/creados.")
except Exception as e:
    logging.error(f"❌ Error al crear directorios de assets: {e}")

"""
Este módulo carga la configuración del sistema Cuentix desde variables de entorno
y define una instancia 'settings' compartida para ser utilizada en todo el backend.
También gestiona la creación inicial de los directorios de assets.
Incluye rutas absolutas útiles: PROJECT_ROOT, BACKEND_DIR, PROMPT_TEMPLATE_PATH.
"""
