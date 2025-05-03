# tasks/generate_story.py
# Orquestador de generación: texto → escenas → video

import os
from concurrent.futures import ThreadPoolExecutor
from core.processors.text_generator import TextGenerator
from core.processors.image_generator import ImageGenerator
from core.processors.audio_generator import AudioGenerator
from core.processors.subtitles_generator import SubtitlesGenerator
from core.processors.video_generator import VideoGenerator
from moviepy.editor import concatenate_videoclips
from utils.helpers import generar_id_unico
from utils.logger import get_logger
from utils.db_memory import STORIES_DB  # Fallback si aún usamos memoria

# ORM: importar sesión y modelo
from config.database import SessionLocal
from models.models import Story

logger = get_logger(__name__)

# Rutas base
ASSETS_DIR = os.path.abspath("assets")
TEXT_DIR = os.path.join(ASSETS_DIR, "Text")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
SUBTITLES_DIR = os.path.join(ASSETS_DIR, "subtitles")
VIDEO_DIR = os.path.join(ASSETS_DIR, "videos")

# Asegurar que los directorios existen
for path in [TEXT_DIR, IMAGES_DIR, AUDIO_DIR, SUBTITLES_DIR, VIDEO_DIR]:
    os.makedirs(path, exist_ok=True)

def procesar_escena(parrafo, image_generator, audio_generator, subtitle_generator, video_generator):
    """
    Genera imagen, audio, subtítulo y clip de video para una escena (párrafo).
    Devuelve el clip o None si falla.
    """
    if not parrafo.strip():
        return None

    try:
        escena_id = generar_id_unico()
        ruta_imagen = os.path.join(IMAGES_DIR, f"{escena_id}.png")
        ruta_audio = os.path.join(AUDIO_DIR, f"{escena_id}.mp3")
        ruta_subtitulo = os.path.join(SUBTITLES_DIR, f"{escena_id}.srt")

        # Generar recursos individuales
        image_generator.generate_image(parrafo, ruta_imagen)
        audio_generator.generate_audio(parrafo, ruta_audio)
        subtitle_generator.generar_subtitulo(ruta_audio, ruta_subtitulo)

        # Crear el clip final para esta escena
        clip = video_generator.create_clip(ruta_imagen, ruta_audio, parrafo)
        return clip

    except Exception as e:
        logger.warning(f"⚠️ Error procesando escena: {e}")
        return None

def generate_story(story_id, user_data):
    """
    Orquesta la generación completa de una historia (texto → video).
    """
    logger.info(f"🚀 Iniciando generación de historia {story_id}")

    # Crear generadores
    text_generator = TextGenerator()
    image_generator = ImageGenerator()
    audio_generator = AudioGenerator()
    subtitle_generator = SubtitlesGenerator()
    video_generator = VideoGenerator()

    # Conectar a la base de datos
    db = SessionLocal()
    story = None

    try:
        # Buscar la historia en la base de datos
        story = db.query(Story).filter_by(id=story_id).first()

        # Si no existe (por fallback), usar la versión en memoria
        if story is None:
            logger.warning("⚠️ Historia no encontrada en la base de datos. Usando STORIES_DB.")
            story = STORIES_DB.get(story_id)
            if story is None:
                logger.error("❌ Historia no encontrada ni en BD ni en memoria.")
                return

        # Cambiar estado a "generating"
        story.status = "generating"
        if db: db.commit()

        # Construir prompt a partir de los datos
        prompt = (
            f"Crea un cuento para un niño o niña de {user_data['edad']} años llamado {user_data['nombre']}. "
            f"El personaje principal será {user_data['personaje_principal']}, quien vive en {user_data['lugar']}. "
            f"Durante la historia encontrará {user_data['objeto_magico']}, que le ayudará a enfrentarse a {user_data['villano']}. "
            f"El final debe ser {user_data['tipo_final']}, y el cuento debe tener un mensaje positivo, ser divertido, fácil de entender y adecuado para la edad del niño o niña."
        )
        logger.info(f"📖 Prompt construido:\n{prompt}")

        # Generar el texto completo
        cuento_completo = text_generator.generate_text(prompt)

        # Guardar el texto generado (opcional)
        with open(os.path.join(TEXT_DIR, f"{story_id}_cuento.txt"), "w", encoding="utf-8") as f:
            f.write(cuento_completo)

        # Dividir en escenas
        parrafos = cuento_completo.strip().split("\n")

        # Procesar escenas en paralelo
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(
                    procesar_escena,
                    parrafo,
                    image_generator,
                    audio_generator,
                    subtitle_generator,
                    video_generator
                )
                for parrafo in parrafos if parrafo.strip()
            ]
            clips = [f.result() for f in futures if f.result()]

        if not clips:
            raise Exception("❌ No se pudo generar ningún clip válido.")

        # Generar el video final
        video_final = concatenate_videoclips(clips)
        ruta_video = os.path.join(VIDEO_DIR, f"{story_id}.mp4")
        video_final.write_videofile(ruta_video, fps=24, verbose=False, logger=None)

        # Guardar la ruta y estado
        story.video_path = ruta_video
        story.status = "completed"
        if db: db.commit()
        logger.info(f"✅ Historia {story_id} generada exitosamente.")

    except Exception as e:
        logger.error(f"❌ Error al generar historia {story_id}: {e}")
        if story:
            story.status = "failed"
            if hasattr(story, 'error_message'):
                story.error_message = str(e)
            if db: db.commit()
    finally:
        db.close()
