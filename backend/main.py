# backend/main.py
# Punto de entrada del sistema. Coordina la generación del video cuento completo (texto, imagen, audio, subtítulo y video).

import os
import sys
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv  # NUEVO
from app import app  # Importa la app Flask desde app.py

# Cargar variables de entorno
load_dotenv()

# Añadimos la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importamos generadores y helpers
from core.processors.text_generator import TextGenerator
from core.processors.audio_generator import AudioGenerator
from core.processors.image_generator import ImageGenerator
from core.processors.video_generator import VideoGenerator
from core.processors.subtitles_generator import SubtitlesGenerator
from moviepy.editor import concatenate_videoclips
from utils.helpers import generar_id_unico
from utils.logger import get_logger

logger = get_logger(__name__)

# Rutas dinámicas tomadas del .env
ASSETS_DIR = os.getenv('ASSETS_DIR', 'assets/')
VIDEO_DIR = os.getenv('VIDEO_DIR', os.path.join(ASSETS_DIR, 'videos'))
TEXT_DIR = os.path.join(ASSETS_DIR, 'Text')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
AUDIO_DIR = os.path.join(ASSETS_DIR, 'audio')
SUBTITLES_DIR = os.path.join(ASSETS_DIR, 'subtitles')

def validar_entrada(prompt: str) -> bool:
    """
    Verifica que el prompt no esté vacío ni demasiado corto.
    """
    return bool(prompt and len(prompt.strip()) > 10)

def procesar_escena(parrafo: str, image_generator, audio_generator, subtitle_generator, video_generator) -> object:
    """
    Genera imagen, audio, subtítulo y clip de video para un párrafo dado.
    Retorna el clip generado o None si el párrafo está vacío.
    """
    if not parrafo.strip():
        return None

    id_escena = generar_id_unico()

    ruta_imagen = os.path.join(IMAGES_DIR, f"{id_escena}.png")
    ruta_audio = os.path.join(AUDIO_DIR, f"{id_escena}.mp3")
    ruta_subtitulo = os.path.join(SUBTITLES_DIR, f"{id_escena}.srt")

    image_generator.generate_image(parrafo, ruta_imagen)
    audio_generator.generate_audio(parrafo, ruta_audio)
    subtitle_generator.generar_subtitulo(ruta_audio, ruta_subtitulo)
    clip = video_generator.create_clip(ruta_imagen, ruta_audio, parrafo)

    return clip

def main():
    # Instanciar los generadores
    text_generator = TextGenerator()
    audio_generator = AudioGenerator()
    image_generator = ImageGenerator()
    video_generator = VideoGenerator()
    subtitle_generator = SubtitlesGenerator()

    # Prompt base para la historia
    prompt = (
        "Crea un cuento corto para niños de 5 años con un mensaje sobre la amistad. "
        "Debe tener un tono divertido, personajes animales, y un final feliz."
    )

    if not validar_entrada(prompt):
        logger.error("❌ El prompt proporcionado no es válido. Debe tener al menos 10 caracteres.")
        return

    cuento_completo = text_generator.generate_text(prompt)

    if len(cuento_completo.strip().split()) < 30:
        logger.warning("⚠️ El cuento generado parece demasiado corto.")

    os.makedirs(TEXT_DIR, exist_ok=True)
    try:
        with open(os.path.join(TEXT_DIR, "cuento_completo.txt"), "w", encoding="utf-8") as f:
            f.write(cuento_completo)
    except Exception as e:
        logger.error(f"❌ Error al guardar el cuento: {e}")
        return

    parrafos = cuento_completo.strip().split("\n")

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(procesar_escena, p, image_generator, subtitle_generator, audio_generator, video_generator)
            for p in parrafos if p.strip()
        ]
        clips = [f.result() for f in futures if f.result() is not None]

    if not clips:
        logger.warning("⚠️ No se generaron clips. Revisa si el texto del cuento fue válido.")
        return

    os.makedirs(VIDEO_DIR, exist_ok=True)
    video_final = concatenate_videoclips(clips)
    video_final.write_videofile(os.path.join(VIDEO_DIR, "cuento_completo.mp4"), fps=24)

    print("\n✅ ¡Video generado exitosamente!\n")

if __name__ == "__main__":
    app.run(debug=True)
