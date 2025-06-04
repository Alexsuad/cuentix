# ──────────────────────────────────────────────────────────────────────────────
# File: backend/main_mvp_audio_unico.py
# Descripción: Script de prueba local del MVP Cuentix que genera un videocuento
# completo usando el pipeline reutilizable (audio único + subtítulos + imágenes).
# ──────────────────────────────────────────────────────────────────────────────

import sys
import os
import uuid

# ────────────────────────────────────────────────────────────────────
# Ajustar sys.path para importar módulos del backend
# (necesario sólo cuando ejecutas este archivo directamente)
# ────────────────────────────────────────────────────────────────────
current_dir = os.path.dirname(os.path.abspath(__file__))  # ruta de este script
backend_dir = os.path.join(current_dir, '..')             # subir a /backend
sys.path.insert(0, backend_dir)                           # priorizar en sys.path
# ────────────────────────────────────────────────────────────────────

# ────────────────────────────────────────────────────────────────────
# Importar módulos del backend
# ────────────────────────────────────────────────────────────────────
from config.settings import settings            # Config centralizada
from utils.logger import get_logger             # Logger de proyecto
from core.orchestrators.story_pipeline import run_pipeline  # 🧩 Nuevo pipeline
# ────────────────────────────────────────────────────────────────────

# ────────────────────────────────────────────────────────────────────
# Inicialización
# ────────────────────────────────────────────────────────────────────
logger = get_logger(__name__)

# Crear carpetas de assets si no existen (seguridad antes de generar archivos)
try:
    os.makedirs(settings.AUDIO_DIR, exist_ok=True)
    os.makedirs(settings.SUBTITLES_DIR, exist_ok=True)
    os.makedirs(settings.IMAGES_DIR, exist_ok=True)
    os.makedirs(settings.VIDEOS_DIR, exist_ok=True)
    logger.info("✅ Directorios de assets verificados/creados.")
except Exception as e:
    logger.error(f"❌ Error al crear directorios de assets: {e}")
    sys.exit(1)
# ────────────────────────────────────────────────────────────────────

# ────────────────────────────────────────────────────────────────────
# Ejecución de prueba local
# ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("🚀 Iniciando pipeline de generación de video-cuento (MVP)…")

    # Datos simulados que vendrían del frontend
    datos_usuario = {
        "nombre": "Leo",
        "edad": 5,
        "personaje_principal": "un valiente caballero",
        "lugar": "un castillo en las nubes",
        "objeto_magico": "una espada brillante",
        "villano": "un dragón dormilón",
        "tipo_final": "un final feliz con amigos"
    }
    logger.info(f"👤 Datos de usuario de prueba: {datos_usuario}")

    story_id = uuid.uuid4().hex[:8]  # ID único para esta historia

    try:
        video_path = run_pipeline(story_id, datos_usuario)
        logger.info(f"🎉 Video listo: {video_path}")
    except Exception as e:
        logger.error(f"❌ Error en pipeline: {e}")
        sys.exit(1)

    logger.info("\n🎬 ¡Pipeline de generación completado con éxito!")
    logger.info(f"📼 Video final disponible en: {video_path}")
