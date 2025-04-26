# tests/test_text_generator.py

# Este test verifica que el generador de texto crea un cuento estructurado y no vacío.

import pytest
from core.processors.text_generator import TextGenerator

@pytest.fixture
def generador_texto():
    """
    Crea una instancia de TextGenerator para usarla en las pruebas.
    """
    return TextGenerator()

def test_generar_texto_basico(generador_texto):
    """
    Verifica que el cuento generado tenga estructura básica y contenido válido.
    """
    # Datos de prueba simulando la entrada de un niño en el frontend
    datos_prueba = {
        "nombre": "Lucas",
        "edad": 6,
        "personaje_principal": "Dragón",
        "lugar": "Bosque encantado",
        "villano": "Robot descontrolado",
        "objeto_magico": "Lupa mágica",
        "tipo_final": "Final feliz"
    }

    # Llamar al generador de cuentos
    resultado = generador_texto.generar_cuento(datos_prueba)

    # Validar que se obtuvo un texto
    assert isinstance(resultado, str), "La función debe devolver un string."
    assert len(resultado) > 20, "El cuento generado debe tener contenido suficiente."

    # Validar que incluye las etiquetas de estructura
    assert any(seccion in resultado for seccion in ["[Intro]", "[Conflicto]", "[Resolucion]", "[Moraleja]"]), \
        "El cuento debe contener las secciones estructuradas [Intro], [Conflicto], [Resolucion], [Moraleja]."
