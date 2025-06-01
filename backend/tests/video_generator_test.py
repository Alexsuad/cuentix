# ──────────────────────────────────────────────────────────────────────────────
# File: backend/tests/video_generator_test.py
# Descripción: Prueba de integración para una escena individual del cuento.
# Genera imagen, audio y subtítulos de una sola escena y ensambla un video sincronizado.
# Esta prueba no se usa en el MVP de audio único, pero es útil para depuración modular.
# ──────────────────────────────────────────────────────────────────────────────

import sys
import uuid
from pathlib import Path

# Ajuste de sys.path para permitir importar desde /backend
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

# ──────────────────────────────────────────────────────────────────────────────
# Bloque principal de prueba
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("🧪 Iniciando prueba de generación de escena individual...")

    # Texto de ejemplo para una escena de prueba
    escena_texto = "Luna era una hada con alas de cristal. Vivía en una nube donde llovían caramelos."

    # ID único para nombrar los archivos de esta ejecución
    scene_id = uuid.uuid4().hex

    # Construcción de rutas absolutas usando settings del sistema
    image_path = Path(settings.IMAGES_DIR) / f"test_img_{scene_id}.png"
    audio_path = Path(settings.AUDIO_DIR) / f"test_audio_{scene_id}.mp3"
    sub_path = Path(settings.SUBTITLES_DIR) / f"test_sub_{scene_id}.srt"
    video_path = Path(settings.VIDEOS_DIR) / f"test_video_{scene_id}.mp4"

    # Instanciar generadores de imagen, audio y subtítulos
    img_gen = ImageGenerator()
    audio_gen = AudioGenerator(motor=settings.TTS_ENGINE)
    sub_gen = SubtitlesGenerator(model_size=settings.WHISPER_MODEL_SIZE)

    # Paso 1: Generar imagen (prompt adaptado para DALL·E)
    logger.info("1️⃣ Generando imagen...")
    prompt = "Ilustración para niños en estilo dibujo animado: una nube flotante hecha de caramelos sobre un cielo azul"
    imagen = img_gen.generate_image(prompt, str(image_path))

    if not imagen:
        logger.error("❌ Fallo en la generación de la imagen.")
        sys.exit(1)
    logger.info(f"✅ Imagen generada: {image_path}")

    # Paso 2: Generar audio
    logger.info("2️⃣ Generando audio...")
    audio = audio_gen.generate_audio(escena_texto, str(audio_path))

    if not audio:
        logger.error("❌ Fallo en la generación del audio.")
        sys.exit(1)
    logger.info(f"✅ Audio generado: {audio_path}")

    # Paso 3: Generar subtítulos en formato SRT
    logger.info("3️⃣ Generando subtítulos...")
    subtitulo_ok = sub_gen.generar_subtitulos(str(audio_path), str(sub_path))

    if not subtitulo_ok:
        logger.error("❌ Fallo en la generación de los subtítulos.")
        sys.exit(1)
    logger.info(f"✅ Subtítulos generados: {sub_path}")

    # Paso 4: Convertir subtítulos SRT a estructura JSON
    logger.info("4️⃣ Convirtiendo subtítulos a JSON...")
    subtitulos_json = srt_to_json_simple(str(sub_path))

    if not subtitulos_json:
        logger.error("❌ Fallo al convertir subtítulos a JSON.")
        sys.exit(1)
    logger.info(f"✅ Subtítulos convertidos a JSON. Total: {len(subtitulos_json)} bloques.")

    # Paso 5: Ensamblar video final con imagen, audio y subtítulos
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
