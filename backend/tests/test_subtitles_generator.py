# tests/test_subtitles_generator.py

import os
import pytest
from core.processors.subtitles_generator import SubtitlesGenerator
from core.processors.audio_generator import AudioGenerator

# Aseguramos que FFmpeg esté disponible en el entorno para Whisper
os.environ["PATH"] += os.pathsep + r"C:\Users\nalex\Herramientas\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

@pytest.fixture
def generador_subtitulo():
    # Crea una instancia de SubtitlesGenerator para usar en el test
    return SubtitlesGenerator()

@pytest.fixture
def generar_audio_temporal():
    # Texto base para generar el audio de prueba
    texto = "Hola, este es un cuento corto para probar subtítulos."
    ruta_audio = os.path.join("assets", "audio", "temp_prueba_subtitulos.mp3")

    # Asegura que la carpeta exista
    os.makedirs(os.path.dirname(ruta_audio), exist_ok=True)

    # Genera el audio
    audio_gen = AudioGenerator()
    resultado = audio_gen.generate_audio(texto, ruta_audio)

    # Valida que el archivo haya sido creado correctamente
    if not os.path.exists(resultado):
        raise FileNotFoundError(f"⚠️ El audio no fue generado correctamente en: {resultado}")

    return resultado

def test_generar_subtitulo_basico(generador_subtitulo, generar_audio_temporal):
    # Usa el audio generado como entrada para probar la transcripción
    ruta_audio = generar_audio_temporal
    ruta_salida = "temp_prueba_subtitulos.srt"

    # Ejecuta el método principal de subtitulación
    resultado = generador_subtitulo.generar_subtitulo(ruta_audio, ruta_salida)

    # Asegura que la función haya devuelto una ruta válida
    assert isinstance(resultado, str), "La función debe retornar una ruta en texto."
    assert os.path.exists(ruta_salida), f"El archivo .srt no fue creado: {ruta_salida}"
    assert ruta_salida.endswith(".srt"), "La extensión debe ser .srt"

    # Revisa el contenido del archivo SRT
    with open(ruta_salida, encoding="utf-8") as f:
        contenido = f.read()
        assert "-->" in contenido, "El archivo debe contener marcas de tiempo tipo SRT."

    print(f"✅ test_generar_subtitulo_basico pasó. Subtítulo: {ruta_salida}")
