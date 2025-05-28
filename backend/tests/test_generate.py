# backend/tests/test_generate.py
# Ejecuta una prueba completa de generación de video-cuento desde consola

import os
import sys

# ─────────────────────────────────────────────────────────────────────────────
# 📁 Ajuste de sys.path para permitir importaciones desde backend/
# ─────────────────────────────────────────────────────────────────────────────

# Ruta absoluta del archivo actual (tests/)
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, backend_dir)

# ─────────────────────────────────────────────────────────────────────────────
# 🔐 Cargar variables desde el archivo .env en la raíz del proyecto
# ─────────────────────────────────────────────────────────────────────────────

from dotenv import load_dotenv
dotenv_path = os.path.abspath(os.path.join(backend_dir, '..', '.env'))
load_dotenv(dotenv_path)

# ─────────────────────────────────────────────────────────────────────────────
# 📦 Importar módulos del sistema Cuentix
# ─────────────────────────────────────────────────────────────────────────────

from core.processors.text_generator import TextGenerator
from core.processors.audio_generator import AudioGenerator
from core.processors.image_generator import ImageGenerator
from core.processors.video_generator import VideoGenerator
from core.processors.subtitles_generator import SubtitlesGenerator
from moviepy import concatenate_videoclips
from utils.helpers import generar_id_unico
from utils.logger import get_logger

# ─────────────────────────────────────────────────────────────────────────────
# 🗂️ Configuración de rutas
# ─────────────────────────────────────────────────────────────────────────────

ASSETS_DIR = os.getenv("ASSETS_DIR", "assets")
VIDEO_DIR = os.path.join(ASSETS_DIR, "videos")
TEXT_DIR = os.path.join(ASSETS_DIR, "Text")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
SUBTITLES_DIR = os.path.join(ASSETS_DIR, "subtitles")

# 🧠 Instanciar módulos de generación
text_generator = TextGenerator()
image_generator = ImageGenerator()
audio_generator = AudioGenerator()
subtitle_generator = SubtitlesGenerator()
video_generator = VideoGenerator()
logger = get_logger("test_generate")

# ─────────────────────────────────────────────────────────────────────────────
# 🎬 Generación de cada escena
# ─────────────────────────────────────────────────────────────────────────────

def procesar_escena(parrafo: str):
    if not parrafo.strip():
        return None

    escena_id = generar_id_unico()
    ruta_imagen = os.path.join(IMAGES_DIR, f"{escena_id}.png")
    ruta_audio = os.path.join(AUDIO_DIR, f"{escena_id}.mp3")
    ruta_subtitulo = os.path.join(SUBTITLES_DIR, f"{escena_id}.srt")

    logger.info(f"🎬 Escena: {escena_id}")

    image_generator.generate_image(parrafo, ruta_imagen)
    audio_generator.generate_audio(parrafo, ruta_audio)
    subtitle_generator.generar_subtitulo(ruta_audio, ruta_subtitulo)

    return video_generator.create_clip(ruta_imagen, ruta_audio, parrafo)

# ─────────────────────────────────────────────────────────────────────────────
# 🔁 Lógica principal
# ─────────────────────────────────────────────────────────────────────────────

def main():
    logger.info("🧪 Iniciando prueba de generación de video-cuento...")

    # Datos simulados de entrada
    user_data = {
        "nombre": "Luna",
        "edad": 5,
        "personaje_principal": "una conejita curiosa",
        "lugar": "el bosque encantado",
        "villano": "el búho gruñón",
        "objeto_magico": "una flor brillante",
        "tipo_final": "feliz"
    }

    cuento = text_generator.generar_cuento(user_data)

    os.makedirs(TEXT_DIR, exist_ok=True)
    with open(os.path.join(TEXT_DIR, "cuento_test.txt"), "w", encoding="utf-8") as f:
        f.write(cuento)

    parrafos = [p for p in cuento.split("\n") if p.strip()]
    clips = []

    for parrafo in parrafos:
        clip = procesar_escena(parrafo)
        if clip:
            clips.append(clip)

    if not clips:
        logger.error("❌ No se generaron clips.")
        return

    os.makedirs(VIDEO_DIR, exist_ok=True)
    video_final = concatenate_videoclips(clips)
    ruta_salida = os.path.join(VIDEO_DIR, "cuento_test_final.mp4")
    video_final.write_videofile(ruta_salida, fps=24)

    logger.info(f"✅ Video generado con éxito en: {ruta_salida}")

# ─────────────────────────────────────────────────────────────────────────────
# ▶️ Ejecutar si es llamado como script
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
