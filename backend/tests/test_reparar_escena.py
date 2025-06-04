# ──────────────────────────────────────────────────────────────────────────────
# File: backend/tests/test_reparar_escena.py
# Descripción: Repara subtítulos o imágenes faltantes para una escena existente.
# Útil para depuración manual. Requiere indicar el ID de escena al final.
# Ejecutar con: python backend/tests/test_reparar_escena.py
# ──────────────────────────────────────────────────────────────────────────────


import os
from pathlib import Path
from config.settings import settings
from core.processors.subtitles_generator import SubtitlesGenerator
from core.processors.image_generator import ImageGenerator
from utils.logger import get_logger

# Inicializar logger y módulos
logger = get_logger(__name__)
subtitle_gen = SubtitlesGenerator()
image_gen = ImageGenerator()

# Directorios base
AUDIO_DIR = Path(settings.AUDIO_DIR)
SUBT_DIR = Path(settings.SUBTITLES_DIR)
IMG_DIR = Path(settings.IMAGES_DIR)

def reparar_escena(scene_id: str):
    logger.info(f"🔧 Reparando escena: {scene_id}")

    audio_path = AUDIO_DIR / f"{scene_id}.mp3"
    subt_path = SUBT_DIR / f"{scene_id}.srt"
    img_path = IMG_DIR / f"{scene_id}.png"

    if not audio_path.exists():
        logger.error("❌ No se encontró el audio base. No se puede reparar.")
        return

    # Generar subtítulo si falta
    if not subt_path.exists():
        logger.info("📝 Subtítulo faltante. Generando con Whisper...")
        try:
            subtitle_gen.generar_subtitulo(str(audio_path), str(subt_path))
            logger.info("✅ Subtítulo generado.")
        except Exception as e:
            logger.error(f"❌ Error generando subtítulo: {e}")

    # Generar imagen si falta
    if not img_path.exists():
        logger.info("🖼 Imagen faltante. Generando con prompt automático...")
        try:
            prompt = f"Claymation digital 3D illustration for children: Escena correspondiente a {scene_id}, pastel colors, soft shadows"
            image_gen.generate_image(prompt, str(img_path))
            logger.info("✅ Imagen generada.")
        except Exception as e:
            logger.error(f"❌ Error generando imagen: {e}")

# ──────────────────────────────────────────────────────────────────────────────
# ▶️ Ejecutar manualmente (cambiar ID abajo)
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Cambia este ID por la escena que quieras reparar
    scene_id = "test_audio_86893f6b4d6c4e24be158546cc49ad53"
    reparar_escena(scene_id)
