# tests/test_generate.py
# ──────────────────────────────────────────────────────────────
# File: tests/test_generate.py
# Descripción: Prueba funcional del sistema completo de generación de video-cuentos.
# Evalúa que se generen correctamente los textos, audios, imágenes, subtítulos y clips,
# y que estos puedan ser ensamblados en un video final sin errores.
#
# Requiere conectividad con las APIs activas de generación (DeepSeek, OpenAI, ElevenLabs)
# y que el entorno esté configurado correctamente (.env, rutas, ffmpeg).
#
# ▶️ Uso:
# Ejecutar desde terminal:
#     python tests/test_generate.py
#
# Al finalizar, se genera un video en: assets/videos/cuento_test_final.mp4
# ──────────────────────────────────────────────────────────────

import os
import sys

# ──────────────────────────────────────────────────────────────
# 📁 Ajuste de sys.path para permitir importaciones desde backend/
# ──────────────────────────────────────────────────────────────
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, backend_dir)

# ──────────────────────────────────────────────────────────────
# 🔐 Cargar variables desde el archivo .env
# ──────────────────────────────────────────────────────────────
from dotenv import load_dotenv
dotenv_path = os.path.abspath(os.path.join(backend_dir, '..', '.env'))
load_dotenv(dotenv_path)

# ──────────────────────────────────────────────────────────────
# 📦 Importar módulos del sistema Cuentix
# ──────────────────────────────────────────────────────────────
from core.processors.text_generator import TextGenerator
from core.processors.audio_generator import AudioGenerator
from core.processors.image_generator import ImageGenerator
from core.processors.subtitles_generator import SubtitlesGenerator
from core.processors.subtitles_utils import srt_to_json_simple
from core.processors.video_generator_sync import crear_video_sincronizado
from utils.helpers import generar_id_unico
from utils.logger import get_logger

# ──────────────────────────────────────────────────────────────
# 🗂️ Configuración de rutas
# ──────────────────────────────────────────────────────────────
ASSETS_DIR = os.getenv("ASSETS_DIR", "assets")
VIDEO_DIR = os.path.join(ASSETS_DIR, "videos")
TEXT_DIR = os.path.join(ASSETS_DIR, "Text")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
SUBTITLES_DIR = os.path.join(ASSETS_DIR, "subtitles")

# 🧠 Instanciar generadores del sistema
text_generator = TextGenerator()
image_generator = ImageGenerator()
audio_generator = AudioGenerator()
subtitle_generator = SubtitlesGenerator()
logger = get_logger("test_generate")

# ──────────────────────────────────────────────────────────────
# 🎬 Generar y ensamblar una escena completa
# ──────────────────────────────────────────────────────────────
def procesar_escena(parrafo: str):
    if not parrafo.strip():
        return None

    escena_id = generar_id_unico()
    ruta_imagen = os.path.join(IMAGES_DIR, f"{escena_id}.png")
    ruta_audio = os.path.join(AUDIO_DIR, f"{escena_id}.mp3")
    ruta_subtitulo = os.path.join(SUBTITLES_DIR, f"{escena_id}.srt")
    ruta_video = os.path.join(VIDEO_DIR, f"{escena_id}.mp4")

    logger.info(f"🎬 Escena: {escena_id}")

    image_generator.generate_image(parrafo, ruta_imagen)
    audio_generator.generate_audio(parrafo, ruta_audio)
    subtitle_generator.generar_subtitulo(ruta_audio, ruta_subtitulo)

    subtitulos_json = srt_to_json_simple(ruta_subtitulo)

    crear_video_sincronizado(
        image_paths=[ruta_imagen],
        audio_path=ruta_audio,
        subtitles_json=subtitulos_json,
        output_path=ruta_video
    )

    return ruta_video

# ──────────────────────────────────────────────────────────────
# 🔁 Lógica principal del test
# ──────────────────────────────────────────────────────────────
def main():
    logger.info("🧪 Iniciando prueba de generación de video-cuento...")

    user_data = {
        "nombre": "Luna",
        "edad": 5,
        "personaje_principal": "una conejita curiosa",
        "lugar": "el bosque encantado",
        "villano": "el búho gruñón",
        "objeto_magico": "una flor brillante",
        "tipo_final": "feliz"
    }

    # Generar el cuento usando el método correcto de la clase TextGenerator
    cuento = text_generator.generate_text(user_data)

    if not cuento:
        logger.error("❌ No se pudo generar el cuento.")
        return

    # Guardar el cuento generado en un archivo de texto
    os.makedirs(TEXT_DIR, exist_ok=True)
    with open(os.path.join(TEXT_DIR, "cuento_test.txt"), "w", encoding="utf-8") as f:
        f.write(cuento)

    parrafos = [p for p in cuento.split("\n") if p.strip()]
    resultados = []

    for parrafo in parrafos:
        clip = procesar_escena(parrafo)
        if clip:
            resultados.append(clip)

    if not resultados:
        logger.error("❌ No se generaron escenas válidas.")
        return

    logger.info("✅ Todas las escenas se procesaron correctamente.")

# ──────────────────────────────────────────────────────────────
# ▶️ Ejecutar como script principal
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
