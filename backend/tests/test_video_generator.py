# tests/test_video_generator.py
# ─────────────────────────────────────────────────────────────
# File: tests/test_video_generator.py
# Propósito: Prueba de integración modular para validar que los módulos de
# imagen, audio, subtítulos y video trabajan en conjunto correctamente.
# Ejecuta una generación básica y produce un archivo .mp4 como resultado final.
# Uso:
#     python3 backend/tests/test_video_generator.py
# ────────────────────────────────────────────────────────────

import sys
import uuid
from pathlib import Path

# Ajuste de sys.path para importar desde /backend
backend_dir = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, backend_dir)

# Importaciones del sistema Cuentix
from config.settings import settings
from utils.logger import get_logger
from core.processors.image_generator import ImageGenerator
from core.processors.audio_generator import AudioGenerator
from core.processors.subtitles_generator import SubtitlesGenerator
from core.processors.subtitles_utils import srt_to_json_simple
from core.processors.video_generator_sync import crear_video_sincronizado

logger = get_logger(__name__)

# ───────────────────────────────────────────────────
# Func. auxiliar: aplicar_efecto_movimiento (zoom_in simple por tiempo)
# ──────────────────────────────────────────────────

def aplicar_efecto_movimiento(clip, tipo="zoom_in"):
    if tipo == "zoom_in":
        return clip.with_position(("center", "center")).with_scale(lambda t: 1.0 + 0.05 * t)
    return clip

# ──────────────────────────────────────────────────
# Prueba completa: generar imagen, audio, subtítulos y ensamblar video
# ──────────────────────────────────────────────────

if __name__ == "__main__":
    logger.info("🧪 Iniciando prueba de generación de escena individual...")

    escena_texto = "Luna era una hada con alas de cristal. Vivía en una nube donde llovían caramelos."
    scene_id = uuid.uuid4().hex

    image_path = Path(settings.IMAGES_DIR) / f"test_img_{scene_id}.png"
    audio_path = Path(settings.AUDIO_DIR) / f"test_audio_{scene_id}.mp3"
    sub_path = Path(settings.SUBTITLES_DIR) / f"test_sub_{scene_id}.srt"
    video_path = Path(settings.VIDEOS_DIR) / f"test_video_{scene_id}.mp4"

    img_gen = ImageGenerator()
    audio_gen = AudioGenerator(motor=settings.TTS_ENGINE)
    sub_gen = SubtitlesGenerator(model_size=settings.WHISPER_MODEL_SIZE)

    logger.info("1️⃣ Generando imagen...")
    prompt = "Ilustración para niños en estilo dibujo animado: una nube flotante hecha de caramelos sobre un cielo azul"
    imagen = img_gen.generate_image(prompt, str(image_path))

    if not imagen:
        logger.error("❌ Fallo en la generación de la imagen.")
        sys.exit(1)
    logger.info(f"✅ Imagen generada: {image_path}")

    logger.info("2️⃣ Generando audio...")
    audio = audio_gen.generate_audio(escena_texto, str(audio_path))

    if not audio:
        logger.error("❌ Fallo en la generación del audio.")
        sys.exit(1)
    logger.info(f"✅ Audio generado: {audio_path}")

    logger.info("3️⃣ Generando subtítulos...")
    subtitulo_ok = sub_gen.generar_subtitulos(str(audio_path), str(sub_path))

    if not subtitulo_ok:
        logger.error("❌ Fallo en la generación de los subtítulos.")
        sys.exit(1)
    logger.info(f"✅ Subtítulos generados: {sub_path}")

    logger.info("4️⃣ Convirtiendo subtítulos a JSON...")
    subtitulos_json = srt_to_json_simple(str(sub_path))

    if not subtitulos_json:
        logger.error("❌ Fallo al convertir subtítulos a JSON.")
        sys.exit(1)
    logger.info(f"✅ Subtítulos convertidos a JSON. Total: {len(subtitulos_json)} bloques.")

    logger.info("5️⃣ Ensamblando video final...")
    video_final = crear_video_sincronizado(
        image_paths=[str(image_path)],
        audio_path=str(audio_path),
        subtitles_json=subtitulos_json,
        output_path=str(video_path)
    )

    if not video_final:
        logger.error("❌ Fallo en el ensamblaje del video.")
        sys.exit(1)
    logger.info(f"🎬 Video final generado exitosamente: {video_path}")
