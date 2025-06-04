# ──────────────────────────────────────────────────────────────────────────────
# File: backend/core/processors/subtitles_generator.py
# Propósito: Generar subtítulos (.srt) a partir de un archivo de audio
#            empleando Whisper. También permite combinar múltiples .srt en uno solo.
# ──────────────────────────────────────────────────────────────────────────────

# ╭─────────────────────────────── Importaciones ───────────────────────────────╮
from pathlib import Path                          # Manejo de rutas multiplataforma
import os                                         # Operaciones con archivos (borrado)
import whisper                                    # Modelo de reconocimiento de voz de OpenAI
from utils.logger import get_logger              # Logger centralizado
from config.settings import settings             # Configuración general del sistema
# ╰─────────────────────────────────────────────────────────────────────────────╯

logger = get_logger(__name__)  # Inicializa el logger para este módulo

# ──────────────────────────────────────────────────────────────────────────────
# Clase principal: SubtitlesGenerator
# Transcribe un audio a subtítulos en formato .srt usando Whisper (local).
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

    _model_cache: dict[str, whisper.Whisper] = {}  # Cache global de modelos cargados

    def __init__(self, model_size: str | None = None) -> None:
        """
        Inicializa la clase y carga (o reutiliza) el modelo Whisper indicado.
        """
        self.model_size: str = model_size or settings.WHISPER_MODEL_SIZE or "base"

        if self.model_size in SubtitlesGenerator._model_cache:
            self.model = SubtitlesGenerator._model_cache[self.model_size]
            logger.info(f"🧠 Whisper «{self.model_size}» reutilizado desde caché.")
        else:
            try:
                logger.info(f"🧠 Cargando Whisper «{self.model_size}» …")
                self.model = whisper.load_model(self.model_size)
                SubtitlesGenerator._model_cache[self.model_size] = self.model
                logger.info("✅ Modelo cargado correctamente.")
            except Exception as e:
                logger.error(f"❌ No se pudo cargar Whisper ({self.model_size}): {e}")
                raise RuntimeError(f"Whisper no disponible: {e}") from e

    def generar_subtitulos(self, ruta_audio: str, ruta_salida: str) -> str:
        """
        Genera un archivo .srt con subtítulos a partir de un audio.
        """
        ruta_audio = Path(ruta_audio)
        ruta_salida = Path(ruta_salida)

        if not ruta_audio.is_file():
            logger.error(f"❌ Audio no encontrado: {ruta_audio}")
            return ""

        try:
            logger.info("🎧 Transcribiendo audio…")
            resultado = self.model.transcribe(str(ruta_audio), verbose=False)
            ruta_salida.parent.mkdir(parents=True, exist_ok=True)

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
                        logger.warning(f"⚠️ Segmento {i} omitido: {seg_e}")

            logger.info("✅ Subtítulos generados correctamente.")
            return str(ruta_salida)

        except Exception as e:
            logger.error(f"❌ Error durante la transcripción: {e}")
            return ""

    generar_subtitulo = generar_subtitulos  # Alias compatible con otros módulos

    @staticmethod
    def _fmt(segundos: float) -> str:
        """
        Convierte un número de segundos a formato SRT (hh:mm:ss,mmm).
        """
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        seg = int(segundos % 60)
        ms = int((segundos - int(segundos)) * 1000)
        return f"{horas:02}:{minutos:02}:{seg:02},{ms:03}"

# ──────────────────────────────────────────────────────────────────────────────
# Función auxiliar: combinar_srt
# Une múltiples archivos .srt individuales en uno solo (cuento completo).
# ──────────────────────────────────────────────────────────────────────────────
def combinar_srt(sub_paths: list[str], salida: str, borrar_originales: bool = False) -> None:
    """
    Une varios archivos SRT individuales en un solo archivo combinado con numeración secuencial.

    Parámetros:
    ------------
    sub_paths : list[str]
        Lista de rutas absolutas a los archivos .srt de cada escena.
    salida : str
        Ruta absoluta donde se guardará el archivo combinado final (cuento_completo.srt).
    borrar_originales : bool
        Si es True, borra los archivos SRT individuales después de combinarlos.
    """
    logger.info(f"🧩 Combinando subtítulos en {salida}…")
    contador = 1
    salida_path = Path(salida)

    try:
        salida_path.parent.mkdir(parents=True, exist_ok=True)

        with salida_path.open("w", encoding="utf-8") as final:
            for path_str in sub_paths:
                path = Path(path_str)
                if not path.exists():
                    logger.warning(f"⚠️ Archivo SRT no encontrado: {path}")
                    continue

                bloques = path.read_text(encoding="utf-8").strip().split("\n\n")
                for bloque in bloques:
                    lineas = bloque.strip().split("\n")
                    if len(lineas) >= 2:
                        final.write(f"{contador}\n")
                        final.write('\n'.join(lineas[1:]))  # Excluye número original
                        final.write('\n\n')
                        contador += 1

                if borrar_originales:
                    try:
                        os.remove(path)
                        logger.info(f"🗑️ SRT eliminado: {path}")
                    except Exception as del_e:
                        logger.warning(f"⚠️ No se pudo eliminar {path}: {del_e}")

        logger.info(f"✅ Subtítulos combinados exitosamente en: {salida}")

    except Exception as e:
        logger.error(f"❌ Error combinando subtítulos: {e}")
