# core/processors/video_generator.py

from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip
from utils.logger import get_logger

logger = get_logger(__name__)

class VideoGenerator:
    """
    Esta clase combina imagen, audio y texto para crear un clip de video
    usando moviepy. Se usa una imagen fija con audio narrado y texto opcional.
    """

    def create_clip(self, ruta_imagen: str, ruta_audio: str, texto: str) -> CompositeVideoClip:
        """
        Crea un videoclip a partir de una imagen, un archivo de audio y texto.

        Parámetros:
        - ruta_imagen (str): Ruta a la imagen de fondo.
        - ruta_audio (str): Ruta al archivo de audio narrado.
        - texto (str): Texto del párrafo que será mostrado como subtítulo.

        Retorna:
        - CompositeVideoClip: Clip de video listo para ser unido con otros clips.
        """

        try:
            logger.info(f"Creando clip de video para: {ruta_imagen}")

            # Cargamos la imagen como clip de fondo
            imagen_clip = ImageClip(ruta_imagen)

            # Cargamos el audio narrado
            audio_clip = AudioFileClip(ruta_audio)

            # Ajustamos duración de la imagen al audio
            imagen_clip = imagen_clip.set_duration(audio_clip.duration)

            # Redimensionamos la imagen a un tamaño de video estándar
            imagen_clip = imagen_clip.resize(height=720)

            # Añadimos el audio al clip
            imagen_clip = imagen_clip.set_audio(audio_clip)

            # Creamos el subtítulo como texto superpuesto
            subtitulo = TextClip(texto, fontsize=30, color='white', font="Arial-Bold", method="caption", size=(1080, None))
            subtitulo = subtitulo.set_duration(audio_clip.duration)
            subtitulo = subtitulo.set_position(("center", "bottom")).margin(bottom=30)

            # Combinamos imagen + texto + audio
            video_clip = CompositeVideoClip([imagen_clip, subtitulo])

            return video_clip

        except Exception as e:
            logger.error(f"Error creando clip de video: {str(e)}")
            return None
