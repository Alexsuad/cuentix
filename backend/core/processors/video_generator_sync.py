# ──────────────────────────────────────────────────────────────────────────────
# File: backend/core/processors/video_generator_sync.py
# Propósito: Ensambla un video sincronizado usando una pista de audio completa,
# subtítulos en formato JSON y una imagen por fragmento narrado.
# Utiliza MoviePy (v2) para crear un video con composición visual y sonora.
# ──────────────────────────────────────────────────────────────────────────────

# ────────────────────────────────────────────────────────────────────
# ✅ CORRECCIÓN: Importar clases directamente desde el paquete moviepy (API v2.x)
# ────────────────────────────────────────────────────────────────────
# Eliminar la línea 'from moviepy.editor import (' y las subsiguientes
# y reemplazar por esta única línea:
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip
# ────────────────────────────────────────────────────────────────────

from pathlib import Path
from utils.logger import get_logger
logger = get_logger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Función principal: crear_video_sincronizado
# Ensambla un video usando audio completo, subtítulos y una imagen por segmento.
# ──────────────────────────────────────────────────────────────────────────────
def crear_video_sincronizado(image_paths: list, audio_path: str, subtitles_json: list, output_path: str) -> str:
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
        # Cargar pista de audio y obtener duración total
        audio_clip = AudioFileClip(audio_path)
        duracion_total = audio_clip.duration
        clips = []

        # Validación de coherencia entre imágenes y subtítulos
        if len(image_paths) != len(subtitles_json):
            logger.warning("⚠️ La cantidad de imágenes no coincide con los bloques de subtítulo. Se usará el mínimo común.")

        # Crear clips de imagen sincronizados con los subtítulos
        for i, (img_path, sub) in enumerate(zip(image_paths, subtitles_json)):
            try:
                start = sub["start"]
                end = sub["end"]
                duracion = end - start

                # ✅ Usar métodos with_... de MoviePy v2.x
                img_clip = ImageClip(img_path).with_start(start).with_duration(duracion)
                clips.append(img_clip)
            except Exception as e:
                logger.warning(f"⚠️ Error al procesar imagen '{img_path}': {e}")

        # Crear subtítulos como clips de texto (alineados con los tiempos)
        for sub in subtitles_json:
            try:
                # ✅ Usar 'txt' para el contenido del texto y 'fontsize' para el tamaño
                # ✅ Usar método 'label' para evitar conflictos de argumentos en 'caption'
                txt_clip = TextClip(
                    txt=sub["text"], # Usar 'txt' en lugar de 'text' o como argumento posicional
                    fontsize=40, # Usar 'fontsize' en lugar de 'font_size'
                    color="white",
                    font="Arial-Bold", # Asegúrate de que esta fuente esté disponible en el sistema
                    method='label',  # 'label' es más genérico que 'caption' y evita conflictos
                    size=(1080, None),
                    align='South'
                ).with_start(sub["start"]).with_duration(sub["end"] - sub["start"])
                clips.append(txt_clip)
            except Exception as e:
                logger.warning(f"⚠️ Subtítulo omitido por error: {e}")

        # Composición del video con imagen, texto y audio
        # ✅ Usar with_audio de MoviePy v2.x
        video = CompositeVideoClip(clips).with_audio(audio_clip)

        # Asegurar que el directorio de salida exista
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Exportar el video final
        # ✅ Eliminar argumentos 'verbose' y 'logger' que no existen en write_videofile de MoviePy 2.x
        video.write_videofile(
            str(output_file),
            fps=24,
            codec="libx264",
            audio_codec="aac",
            bitrate="800k",
            preset="medium",
            threads=4,
            ffmpeg_params=["-crf", "28"],
            # Eliminar: verbose=False,
            # Eliminar: logger=None
        )

        logger.info(f"✅ Video exportado correctamente en: {output_file}") # Usar output_file para consistencia
        return str(output_file) # Retornar str(output_file) para consistencia

    except Exception as e:
        logger.error(f"❌ Error en la generación del video: {e}")
        return ""