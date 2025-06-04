# ────────────────────────────────────────────────────────────────────────────
# File: backend/main_mvp.py
# Descripción: Script principal para ejecutar el flujo completo del MVP de Cuentix.
# Genera un video-cuento infantil con texto, imágenes, audio, subtítulos y ensamblaje.
# Utiliza datos de prueba desde JSON y muestra logs detallados del proceso.
# ────────────────────────────────────────────────────────────────────────────

import os
import sys
import json
from pathlib import Path
import logging

from utils.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)
import core.processors.text_generator as tg
logger.debug(f"📂 Usando text_generator desde: {tg.__file__}")

from pydub import AudioSegment
import pysrt

sys.path.append(str(Path(__file__).resolve().parent))

from core.processors.text_generator import TextGenerator
from core.validators.campos_requeridos import CAMPOS_REQUERIDOS
from core.processors.image_generator import ImageGenerator
from core.processors.audio_generator import AudioGenerator
from core.processors.subtitles_generator import SubtitlesGenerator, combinar_srt
from core.processors.video_generator_sync import ensamblar_video

def cargar_datos_prueba() -> dict:
    json_path = Path(__file__).parent / "tests" / "test_user_data.json"
    if not json_path.exists():
        logger.error("❌ Archivo de datos de prueba no encontrado: %s", json_path)
        return {}
    with open(json_path, "r", encoding="utf-8") as f:
        datos = json.load(f)
    logger.debug("DEBUG – Contenido cargado desde JSON: %s", datos)
    for campo in CAMPOS_REQUERIDOS:
        if campo not in datos:
            logger.error("❌ Campo obligatorio faltante en test_user_data.json: %s", campo)
            return {}
    return datos

def unir_audios(audio_paths: list, salida: str) -> str:
    audio_completo = AudioSegment.empty()
    for ruta in audio_paths:
        segmento = AudioSegment.from_file(ruta)
        audio_completo += segmento
    audio_completo.export(salida, format="mp3", bitrate="128k")
    return salida

def convertir_subtitulos_a_json(srt_file_path: str) -> list:
    subtitulos = []
    srt_file = pysrt.open(srt_file_path)
    for item in srt_file:
        subtitulos.append({
            "start": item.start.ordinal / 1000,
            "end": item.end.ordinal / 1000,
            "text": item.text
        })
    return subtitulos

if __name__ == "__main__":
    logger.info("🚀 Iniciando generación de video-cuento (MVP)...")

    datos_usuario = cargar_datos_prueba()
    if not datos_usuario:
        logger.error("❌ No se pudo continuar: datos de entrada inválidos.")
        sys.exit(1)

    texto_cuento, escenas = TextGenerator().generar_cuento(datos_usuario)
    if not escenas:
        logger.error("❌ El cuento no tiene escenas. Abortando.")
        sys.exit(1)

    audio_gen = AudioGenerator(motor=settings.AUDIO_ENGINE)
    sub_gen = SubtitlesGenerator(model_size=settings.WHISPER_MODEL_SIZE)
    image_gen = ImageGenerator()

    escenas_multimedia = []

    for idx, texto in enumerate(escenas):
        logger.info(f"🎮 Procesando escena {idx+1}...")
        imagen_path = image_gen.generate_image(texto, str(Path(settings.IMAGES_DIR) / f"scene_{idx+1}.png"))
        audio_path  = audio_gen.generate_audio(texto, str(Path(settings.AUDIO_DIR)  / f"scene_{idx+1}.mp3"))
        subs_path   = sub_gen.generar_subtitulo(audio_path, str(Path(settings.SUBTITLES_DIR) / f"scene_{idx+1}.srt"))
        escenas_multimedia.append({
            "imagen": imagen_path,
            "audio": audio_path,
            "subtitulos": subs_path
        })

    image_paths = [e["imagen"] for e in escenas_multimedia]
    audio_paths = [e["audio"] for e in escenas_multimedia if e["audio"] and Path(e["audio"]).is_file()]
    sub_paths = [e["subtitulos"] for e in escenas_multimedia if e["subtitulos"] and Path(e["subtitulos"]).is_file()]

    ruta_srt_completo = settings.BACKEND_DIR / settings.TEXT_DIR / "cuento_completo.srt"
    combinar_srt(sub_paths, str(ruta_srt_completo), borrar_originales=True)
    logger.info(f"📄 Subtítulos finales listos en: {ruta_srt_completo}")

    audio_path = unir_audios(audio_paths, settings.BACKEND_DIR / settings.AUDIO_DIR / "audio_completo.mp3")
    subtitles_json = convertir_subtitulos_a_json(str(ruta_srt_completo))
    salida_video = ensamblar_video(image_paths, audio_path, subtitles_json, "output/video_final.mp4")

    logger.info("✅ Video cuento generado exitosamente en: %s", salida_video)
    logger.info("🎉 Proceso completo. Puedes reproducir el video generado.")
