
# tests/test_text_generator.py

# Prueba unitaria para verificar que el generador de texto (DeepSeek) devuelve una respuesta válida.

import pytest
from core.processors.text_generator import TextGenerator

@pytest.fixture
def generador_texto():
    return TextGenerator()

def test_generar_texto_basico(generador_texto):
    prompt = "Escribe un cuento para niños sobre la importancia de compartir."
    resultado = generador_texto.generate_text(prompt)

    assert isinstance(resultado, str), "La salida debe ser una cadena de texto."
    assert len(resultado.strip()) > 20, "El texto generado debe tener contenido significativo."
    assert """Lo siento""" not in resultado, "No debe contener mensajes de error en la respuesta."

    print("✅ test_generar_texto_basico pasó correctamente.")

