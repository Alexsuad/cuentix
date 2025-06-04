# tests/test_image_generator.py
# ──────────────────────────────────────────────────────────────
# File: tests/test_image_generator.py
# Prueba unitaria para verificar que se genera una imagen válida
# a partir de un texto usando OpenAI DALL·E. Verifica la creación
# del archivo PNG y su tamaño.
#
# ▶️ Modo de uso:
# Ejecutar desde la raíz del proyecto con pytest:
#   pytest tests/test_image_generator.py
# ──────────────────────────────────────────────────────────────



import os
from pathlib import Path
import pytest
from core.processors.image_generator import ImageGenerator

@pytest.fixture
def generador_imagen():
    return ImageGenerator()

def test_generar_imagen_basica(generador_imagen, tmp_path):
    descripcion = "Un dragón sonriente volando sobre un castillo en el cielo."
    ruta = tmp_path / "test_imagen.png"

    resultado = generador_imagen.generate_image(descripcion, str(ruta))

    assert resultado != "", "La función debe devolver una ruta válida."
    assert Path(resultado).exists(), f"La imagen no fue creada: {resultado}"
    assert resultado.endswith(".png"), "El archivo debe tener extensión PNG."
    assert Path(resultado).stat().st_size > 10000, "La imagen parece vacía o incompleta."

    print(f"✅ test_generar_imagen_basica pasó. Imagen: {resultado}")

