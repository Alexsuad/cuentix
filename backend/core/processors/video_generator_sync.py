# ──────────────────────────────────────────────────────────────────────────────
# File: backend/core/processors/video_generator_sync.py
# Propósito: Ensambla un video sincronizado usando una pista de audio completa,
# subtítulos en formato JSON y una imagen por fragmento narrado.
# Utiliza MoviePy (v2) para crear un video con composición visual y sonora.
# ──────────────────────────────────────────────────────────────────────────────

from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip
from pathlib import Path
from utils.logger import get_logger
logger = get_logger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Función principal: ensamblar_video
# Ensambla un video usando audio completo, subtítulos y una imagen por segmento.
# ──────────────────────────────────────────────────────────────────────────────
def ensamblar_video(image_paths: list, audio_path: str, subtitles_json: list, output_path: str) -> str:
    """
    Genera un video final sincronizado con una pista de audio, subtítulos y una imagen por segmento.

    Parámetros:
    -----------
    image_paths : list
        Lista de rutas a archivos de imagen (una por subtítulo).
    audio_path : str
        Ruta al archivo de audio completo (mp3).
    subtitles_json : list
        Lista de bloques con 'start', 'end', 'text'.
    output_path : str
        Ruta donde se guardará el video final.

    Retorna:
    --------
    str
        Ruta del archivo de video generado, o "" si falla.
    """
    try:
        # Cargar la pista de audio
        audio_clip = AudioFileClip(audio_path)
        duracion_total = audio_clip.duration
        clips = []

        if len(image_paths) != len(subtitles_json):
            logger.warning("⚠️ La cantidad de imágenes no coincide con los bloques de subtítulo. Se usará el mínimo común.")

        for i, (img_path, sub) in enumerate(zip(image_paths, subtitles_json)):
            try:
                start = sub["start"]
                end = sub["end"]
                duracion = end - start

                img_clip = ImageClip(img_path).with_start(start).with_duration(duracion)
                clips.append(img_clip)
            except Exception as e:
                logger.warning(f"⚠️ Error al procesar imagen '{img_path}': {e}")

        for sub in subtitles_json:
            try:
                txt_clip = (TextClip(
                    txt=sub["text"],
                    fontsize=40,
                    color="white",
                    font="DejaVuSans-Bold",
                    method="caption",
                    size=(1080, None))
                    .with_start(sub["start"])
                    .with_duration(sub["end"] - sub["start"])
                    .with_position(("center", "bottom")))
                clips.append(txt_clip)
            except Exception as e:
                logger.warning(f"⚠️ Subtítulo omitido por error: {e}")

        video = CompositeVideoClip(clips).with_audio(audio_clip)

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        video.write_videofile(
            str(output_file),
            fps=24,
            codec="libx264",
            audio_codec="aac",
            bitrate="800k",
            preset="medium",
            threads=4,
            ffmpeg_params=["-crf", "28"]
        )

        logger.info(f"✅ Video exportado correctamente en: {output_file}")

        # Liberar recursos explícitamente
        for c in clips:
            c.close()
        audio_clip.close()
        video.close()

        return str(output_file)

    except Exception as e:
        logger.error(f"❌ Error en la generación del video: {e}")
        return ""
