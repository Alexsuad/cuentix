# backend/core/processors/video_generator.py
# ──────────────────────────────────────────────────────────────────────────────
# Descripción: Ensambla clips de video usando MoviePy (API v2.x)
# - Combina imagen, audio y subtítulos por escena
# - Compatible con Pillow >= 9.2 y MoviePy >= 2.0
# ──────────────────────────────────────────────────────────────────────────────

# Parche para compatibilidad con Pillow ≥10 (por eliminación de ANTIALIAS)
from PIL import Image
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

import os
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx import resize, margin  # ✅ forma correcta # Importación correcta de efectos
from utils.logger import get_logger

logger = get_logger(__name__)

class VideoGenerator:
    """
    Clase encargada de combinar imagen, audio y subtítulos en un clip de video.
    Utiliza MoviePy para crear escenas a partir de ilustraciones generadas,
    narración en audio y subtítulos sincronizados.
    """

    def create_clip(self, ruta_imagen: str, ruta_audio: str, texto: str) -> CompositeVideoClip:
        """
        Crea un videoclip a partir de una imagen, un archivo de audio y texto.

        Parámetros:
        - ruta_imagen (str): Ruta a la imagen de fondo.
        - ruta_audio (str): Ruta al archivo de audio narrado.
        - texto (str): Texto del párrafo que será mostrado como subtítulo.

        Retorna:
        - CompositeVideoClip: Clip de video listo para unirse con otros clips.
        """
        try:
            logger.info(f"Creando clip de video para: {ruta_imagen}")

            # Verificar existencia de archivos requeridos
            if not (ruta_imagen and os.path.exists(ruta_imagen)):
                raise FileNotFoundError(f"Imagen no encontrada: {ruta_imagen}")
            if not (ruta_audio and os.path.exists(ruta_audio)):
                raise FileNotFoundError(f"Audio no encontrado: {ruta_audio}")

            # Crear clip de imagen y aplicar duración + audio
            imagen_clip = ImageClip(ruta_imagen)
            audio_clip = AudioFileClip(ruta_audio)

            imagen_clip = (
                imagen_clip.with_duration(audio_clip.duration)
                           .with_audio(audio_clip)
            )
            imagen_clip = resize.resize(imagen_clip, height=720)  # Redimensionar a 720p

            # Crear clip de subtítulo
            subtitulo = TextClip(
                text=texto,
                font="DejaVuSans-Bold",  # Asegúrate de tener esta fuente instalada
                font_size=30,
                color="white",
                method="caption",
                size=(1080, None)
            ).with_duration(audio_clip.duration) \
             .with_position(("center", "bottom"))
            subtitulo = margin.margin(subtitulo, bottom=30)

            # Componer el clip final con imagen + subtítulo
            video_clip = CompositeVideoClip([imagen_clip, subtitulo])

            # Liberar recursos
            audio_clip.close()

            return video_clip

        except Exception as e:
            logger.error(f"Error creando clip de video: {str(e)}")
            return None
