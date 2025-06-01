# ──────────────────────────────────────────────────────────────────────────────
# File: backend/main_mvp.py
# Descripción: Script maestro para generar un cuento completo (texto, audio,
# subtítulos, imágenes y video) usando los módulos del backend, con flujo lineal.
# Útil para pruebas E2E del pipeline de generación.
# ──────────────────────────────────────────────────────────────────────────────

import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Ajuste de sys.path para importar módulos del proyecto desde la raíz de backend
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, '..')
sys.path.insert(0, backend_dir)

# Importaciones del sistema
from config.settings import settings
from core.processors.text_generator import TextGenerator
from core.processors.audio_generator import AudioGenerator
from core.processors.subtitles_generator import SubtitlesGenerator
from core.processors.image_generator import ImageGenerator
from moviepy.editor import concatenate_videoclips, ImageClip, AudioFileClip
from utils.helpers import generar_id_unico
from utils.logger import get_logger
from utils.prompts import construir_prompt_personalizado

logger = get_logger(__name__)

# Asegurar directorios
os.makedirs(settings.AUDIO_DIR, exist_ok=True)
os.makedirs(settings.SUBTITLES_DIR, exist_ok=True)
os.makedirs(settings.IMAGES_DIR, exist_ok=True)
os.makedirs(settings.VIDEOS_DIR, exist_ok=True)

# Inicializar módulos
text_generator = TextGenerator()
audio_generator = AudioGenerator(motor=settings.TTS_ENGINE)
subtitle_generator = SubtitlesGenerator()
image_generator = ImageGenerator()

# Procesar una escena
def process_scene(scene_text: str, scene_index: int, total_scenes: int, user_data: dict) -> tuple:
    if not scene_text.strip():
        return None, None

    scene_id = generar_id_unico()
    logger.info(f"🎬 Escena {scene_index + 1}/{total_scenes}: {scene_text[:50]}...")

    audio_path = Path(settings.AUDIO_DIR) / f"{scene_id}.mp3"
    subtitle_path = Path(settings.SUBTITLES_DIR) / f"{scene_id}.srt"
    image_path = Path(settings.IMAGES_DIR) / f"{scene_id}.png"

    # Audio
    audio = audio_generator.generate_audio(scene_text, str(audio_path))
    if not audio:
        logger.error(f"❌ Audio fallido en escena {scene_index + 1}.")
        return None, None

    # Subtítulo
    subtitle_generator.generar_subtitulo(audio, str(subtitle_path))

    # Imagen con estilo Cuentix
    prompt = f"Claymation digital 3D illustration for children: {scene_text}, pastel colors, soft shadows"
    imagen = image_generator.generate_image(prompt, str(image_path))
    if not imagen:
        logger.error(f"❌ Imagen fallida en escena {scene_index + 1}.")
        return None, None

    # Duración del audio
    try:
        clip = AudioFileClip(audio)
        duration = clip.duration
        clip.close()
    except Exception as e:
        logger.error(f"❌ Duración de audio fallida: {e}")
        return None, None

    return imagen, duration

# Generación del cuento completo

def generate_full_story_mvp(user_data: dict):
    logger.info("🚀 Iniciando generación de video-cuento (MVP)...")

    prompt = construir_prompt_personalizado(user_data)
    texto = text_generator.generate_text(prompt)
    if not texto or len(texto.strip()) < 50:
        logger.error("❌ Texto generado inválido.")
        return None

    escenas = [p.strip() for p in texto.split("\n") if p.strip()]
    if not escenas:
        logger.error("❌ No hay escenas válidas.")
        return None

    resultados = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_scene, escena, i, len(escenas), user_data)
                   for i, escena in enumerate(escenas)]
        for future in futures:
            try:
                img, dur = future.result()
                if img and dur:
                    resultados.append({"image_path": img, "duration": dur})
            except Exception as e:
                logger.error(f"❌ Error en escena: {e}")

    if not resultados:
        logger.error("❌ No se generaron clips válidos.")
        return None

    clips = []
    for r in resultados:
        try:
            clip = ImageClip(r["image_path"]).with_duration(r["duration"])
            clips.append(clip)
        except Exception as e:
            logger.error(f"❌ Clip inválido: {e}")

    if not clips:
        logger.error("❌ No hay clips para ensamblar.")
        return None

    try:
        video_final = concatenate_videoclips(clips)
    except Exception as e:
        logger.error(f"❌ Fallo en concatenación: {e}")
        return None

    salida = Path(settings.VIDEOS_DIR) / f"{generar_id_unico()}_cuento_final.mp4"
    try:
        logger.info(f"💾 Exportando a: {salida}")
        video_final.write_videofile(
            str(salida),
            fps=24,
            codec="libx264",
            verbose=False,
            logger=None
        )
        logger.info("✅ Video exportado con éxito.")
        return str(salida)
    except Exception as e:
        logger.error(f"❌ Fallo exportando video: {e}")
        return None

# Ejecución manual
if __name__ == "__main__":
    datos_prueba = {
        "nombre": "Leo",
        "edad": 5,
        "personaje_principal": "un valiente caballero",
        "lugar": "un castillo en las nubes",
        "objeto_magico": "una espada brillante",
        "villano": "un dragón dormilón",
        "tipo_final": "un final feliz con amigos"
    }

    ruta_video = generate_full_story_mvp(datos_prueba)
    if ruta_video:
        logger.info(f"\n🎉 ¡Video generado con éxito!\nRuta: {ruta_video}")
    else:
        logger.error("\n❌ El pipeline falló en alguna etapa.")
