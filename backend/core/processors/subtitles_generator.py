# ──────────────────────────────────────────────────────────────────────────────
# File: backend/core/processors/subtitles_generator.py
# Propósito: Generar subtítulos (.srt) a partir de un archivo de audio
#            empleando Whisper. Permite elegir tamaño del modelo ("tiny",
#            "base", "small", "medium", "large") y reutiliza la instancia
#            para evitar recargas innecesarias.
# ──────────────────────────────────────────────────────────────────────────────

# Importaciones estándar y del proyecto
from pathlib import Path
import whisper  # Modelo de reconocimiento de voz de OpenAI
from utils.logger import get_logger  # Logger centralizado
from config.settings import settings  # Configuración general del sistema

logger = get_logger(__name__)  # Inicializa el logger para este módulo

# ──────────────────────────────────────────────────────────────────────────────
# Clase principal: SubtitlesGenerator
# Encargada de transcribir audio a texto y generar un archivo de subtítulos.
# ──────────────────────────────────────────────────────────────────────────────
class SubtitlesGenerator:
    """
    Transcribe un archivo de audio y genera subtítulos en formato .srt.

    Atributos:
    -----------
    model_size : str
        Tamaño del modelo Whisper a utilizar.
    model : whisper.Whisper
        Instancia del modelo Whisper ya cargada (se reutiliza entre llamadas).

    Métodos:
    --------
    generar_subtitulos(ruta_audio, ruta_salida) -> str
        Genera un archivo .srt desde un audio. Retorna la ruta generada o "" si falla.
    """

    # Caché de modelos cargados para evitar duplicar consumo de memoria
    _model_cache: dict[str, whisper.Whisper] = {}

    def __init__(self, model_size: str | None = None) -> None:
        """
        Inicializa la clase y carga (o reutiliza) el modelo Whisper indicado.

        Parámetros:
        ------------
        model_size : str | None
            Tamaño del modelo a usar. Si no se indica, se toma de settings.
        """
        self.model_size: str = model_size or settings.WHISPER_MODEL_SIZE or "base"

        if self.model_size in SubtitlesGenerator._model_cache:
            # Si el modelo ya fue cargado previamente, se reutiliza
            self.model = SubtitlesGenerator._model_cache[self.model_size]
            logger.info(f"🧠 Whisper «{self.model_size}» reutilizado desde caché.")
        else:
            try:
                # Si el modelo no está en caché, se carga desde cero
                logger.info(f"🧠 Cargando Whisper «{self.model_size}» …")
                self.model = whisper.load_model(self.model_size)
                SubtitlesGenerator._model_cache[self.model_size] = self.model
                logger.info("✅ Modelo cargado correctamente.")
            except Exception as e:
                # Error crítico si no se puede cargar el modelo
                logger.error(f"❌ No se pudo cargar Whisper ({self.model_size}): {e}")
                raise RuntimeError(f"Whisper no disponible: {e}") from e

    def generar_subtitulos(self, ruta_audio: str, ruta_salida: str) -> str:
        """
        Genera un archivo .srt con subtítulos a partir de un audio.

        Parámetros:
        ------------
        ruta_audio : str
            Ruta absoluta al archivo de audio (formato .mp3, .wav, etc.).
        ruta_salida : str
            Ruta absoluta donde se guardará el archivo .srt generado.

        Retorna:
        ---------
        str
            Ruta del archivo generado o "" si ocurrió un error.
        """
        ruta_audio = Path(ruta_audio)
        ruta_salida = Path(ruta_salida)

        # Validar que el archivo de audio existe
        if not ruta_audio.is_file():
            logger.error(f"❌ Audio no encontrado: {ruta_audio}")
            return ""

        try:
            # Transcripción del audio usando Whisper
            logger.info("🎧 Transcribiendo audio…")
            resultado = self.model.transcribe(str(ruta_audio), verbose=False)

            # Asegurar que el directorio de salida exista
            ruta_salida.parent.mkdir(parents=True, exist_ok=True)

            # Escritura del archivo .srt con formato estándar
            logger.info(f"💾 Guardando SRT en {ruta_salida}…")
            with ruta_salida.open("w", encoding="utf-8") as f:
                for i, seg in enumerate(resultado["segments"], start=1):
                    try:
                        f.write(
                            f"{i}\n"
                            f"{self._fmt(seg['start'])} --> {self._fmt(seg['end'])}\n"
                            f"{seg['text'].strip()}\n\n"
                        )
                    except Exception as seg_e:
                        # Si falla un segmento, se omite y se continúa
                        logger.warning(f"⚠️ Segmento {i} omitido: {seg_e}")

            logger.info("✅ Subtítulos generados correctamente.")
            return str(ruta_salida)

        except Exception as e:
            # Error general de transcripción o escritura
            logger.error(f"❌ Error durante la transcripción: {e}")
            return ""

    generar_subtitulo = generar_subtitulos  # Alias compatible con otros módulos

    @staticmethod
    def _fmt(segundos: float) -> str:
        """
        Convierte un número de segundos a formato SRT (hh:mm:ss,mmm).

        Parámetros:
        ------------
        segundos : float
            Tiempo en segundos.

        Retorna:
        ---------
        str
            Tiempo formateado como cadena compatible con SRT.
        """
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        seg = int(segundos % 60)
        ms = int((segundos - int(segundos)) * 1000)
        return f"{horas:02}:{minutos:02}:{seg:02},{ms:03}"
