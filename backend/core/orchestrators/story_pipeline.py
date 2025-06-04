# ────────────────────────────────────────────────────────────────
# File: core/orchestrators/story_pipeline.py
# Descripción: Función reutilizable para generar un videocuento
# usando un audio único, subtítulos y sincronización con imágenes.
# ────────────────────────────────────────────────────────────────

from config.settings import settings
from utils.logger import get_logger
from utils.paths import new_asset_path
from config.database import SessionLocal
from models.models import Story
from core.processors.text_generator import TextGenerator
from core.processors.audio_generator import AudioGenerator
from core.processors.subtitles_generator import SubtitlesGenerator
from core.processors.image_generator import ImageGenerator
from core.processors.video_generator_sync import ensamblar_video
from core.processors.subtitles_utils import srt_to_json_simple

logger = get_logger(__name__)

def run_pipeline(story_id: str, datos_usuario: dict) -> str:
    """
    Ejecuta el pipeline completo y devuelve la ruta absoluta del .mp4 generado.
    Lanza Exception en caso de error (el caller decide cómo manejarla).
    """
    db = SessionLocal()
    try:
        historia = db.query(Story).filter_by(id=story_id).first()
        if not historia:
            logger.error(f"❌ Historia con ID {story_id} no encontrada en DB.")
            raise RuntimeError("Historia no encontrada para procesamiento.")

        historia.status = "generating"
        db.commit()

        generator = TextGenerator()
        texto, escenas = generator.generar_cuento(datos_usuario)
        if not texto or len(texto.strip()) < 50:
            historia.status = "failed"
            historia.error_message = "Texto generado vacío o demasiado corto"
            db.commit()
            raise RuntimeError("Texto generado vacío o demasiado corto")

        historia.status = "processing_audio"
        db.commit()

        audio_path = new_asset_path("audio", f"{story_id}.mp3")
        tts = AudioGenerator(motor=settings.TTS_ENGINE)
        tts.generate_audio(texto, audio_path)

        historia.status = "processing_subtitles"
        db.commit()

        srt_path = new_asset_path("subtitles", f"{story_id}.srt")
        whisper = SubtitlesGenerator(model_size=settings.WHISPER_MODEL_SIZE)
        whisper.generar_subtitulos(audio_path, srt_path)
        subt_json = srt_to_json_simple(srt_path)

        historia.status = "processing_images"
        db.commit()

        image_paths = []
        painter = ImageGenerator()
        for i, seg in enumerate(subt_json, start=1):
            prompt = f"Claymation digital 3D illustration for children: {seg['text']}"
            img_path = new_asset_path("images", f"{story_id}_{i:02}.png")
            painter.generate_image(prompt, img_path)
            image_paths.append(img_path)

        if not image_paths:
            historia.status = "failed"
            historia.error_message = "No se generaron imágenes"
            db.commit()
            raise RuntimeError("No se generaron imágenes")

        historia.status = "assembling_video"
        db.commit()

        video_path = new_asset_path("videos", f"{story_id}.mp4")
        ensamblar_video(image_paths, audio_path, subt_json, video_path)

        historia.status = "completed"
        historia.video_path = video_path
        historia.thumbnail_url = image_paths[0] if image_paths else None
        historia.story_text_url = new_asset_path("text", f"{story_id}.txt")
        historia.subtitles_url = new_asset_path("text", f"{story_id}.json")

        with open(historia.story_text_url, "w", encoding="utf-8") as f:
            f.write(texto)

        import json
        with open(historia.subtitles_url, "w", encoding="utf-8") as f:
            json.dump(subt_json, f, ensure_ascii=False, indent=2)

        db.commit()
        logger.info(f"🎉 Video listo: {video_path}")
        return video_path

    except Exception as e:
        logger.error(f"❌ Error en pipeline para story_id {story_id}: {e}")
        if 'historia' in locals():
            historia.status = "failed"
            historia.error_message = str(e)
            db.commit()
        raise

    finally:
        db.close()
