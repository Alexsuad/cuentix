# tests/test_audio_generator.py

# ──────────────────────────────────────────────────────────────
# File: tests/test_audio_generator.py
# Descripción: Prueba unitaria automatizada para validar el módulo
# AudioGenerator del sistema Cuentix. Verifica que, al generar un
# archivo .mp3 con texto de entrada, se cree una salida válida:
# - El archivo se guarda correctamente
# - Tiene contenido (>1 KB)
# - Tiene extensión .mp3
# Compatible con motores como gTTS, ElevenLabs o DeepSeek, según settings.
# ──────────────────────────────────────────────────────────────


# Prueba unitaria para verificar la generación de audio con los motores configurados (gTTS, OpenAI, ElevenLabs)

import os
from pathlib import Path
import pytest
from core.processors.audio_generator import AudioGenerator

@pytest.fixture
def generador_audio():
    return AudioGenerator()

def test_generar_audio_basico(generador_audio, tmp_path):
    # Crear ruta temporal de salida para el archivo de audio
    ruta_salida = tmp_path / "test_audio.mp3"
    texto = "Este es un cuento corto para una prueba de audio."

    # Ejecutar el generador de audio
    resultado = generador_audio.generate_audio(texto, str(ruta_salida))

    # Verificaciones
    assert resultado != "", "La función debe devolver una ruta válida."
    assert Path(resultado).exists(), f"El archivo de audio no se creó: {resultado}"
    assert resultado.endswith(".mp3"), "El archivo debe tener extensión .mp3"
    assert Path(resultado).stat().st_size > 1000, "El archivo no debe estar vacío."

    print(f"✅ test_generar_audio_basico pasó. Ruta: {resultado}")

