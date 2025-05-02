# core/processors/subtitles_generator.py

# Este módulo usa Whisper para transcribir archivos de audio y generar subtítulos en formato .srt.
# Usa el modelo local de Whisper especificado en la variable de entorno WHISPER_MODEL_SIZE.

import os
import whisper
from utils.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)

class SubtitlesGenerator:
    """
    Clase encargada de convertir audio a subtítulos usando Whisper (modelo local).
    """

    def __init__(self):
        self.model_size = settings.WHISPER_MODEL_SIZE or "base"
        logger.info(f"🧠 Cargando modelo Whisper ({self.model_size})...")
        try:
            self.model = whisper.load_model(self.model_size)
        except Exception as e:
            logger.error(f"❌ No se pudo cargar el modelo Whisper: {e}")
            raise

    def generar_subtitulo(self, ruta_audio: str, ruta_salida: str) -> str:
        """
        Transcribe un archivo de audio a subtítulos en formato SRT.
        """
        try:
            if not os.path.exists(ruta_audio):
                raise FileNotFoundError(f"El archivo de audio no existe: {ruta_audio}")
            
            ruta_audio = os.path.abspath(ruta_audio)
            logger.info(f"🔊 Transcribiendo archivo '{ruta_audio}' con modelo Whisper '{self.model_size}'...")
            resultado = self.model.transcribe(ruta_audio, task="transcribe")

            os.makedirs(os.path.dirname(ruta_salida) or ".", exist_ok=True)
            with open(ruta_salida, "w", encoding="utf-8") as f:
                for i, segmento in enumerate(resultado["segments"]):
                    inicio = self._formatear_tiempo(segmento["start"])
                    fin = self._formatear_tiempo(segmento["end"])
                    texto = segmento["text"].strip()
                    f.write(f"{i+1}\n{inicio} --> {fin}\n{texto}\n\n")

            logger.info(f"✅ Subtítulo generado en: {ruta_salida}")
            return ruta_salida

        except Exception as e:
            logger.error(f"❌ Error al generar subtítulo: {e}")
            return ""

    def _formatear_tiempo(self, segundos: float) -> str:
        """
        Convierte segundos a formato SRT hh:mm:ss,ms
        """
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segundos_rest = int(segundos % 60)
        milisegundos = int((segundos - int(segundos)) * 1000)
        return f"{horas:02}:{minutos:02}:{segundos_rest:02},{milisegundos:03}"
