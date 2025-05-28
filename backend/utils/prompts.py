# utils/prompts.py

# Este módulo gestiona la carga y formateo seguro de los prompts de texto para Cuentix.

import os
from pathlib import Path

def cargar_plantilla_prompt(ruta_relativa):
    """
    Carga una plantilla de texto desde una ruta relativa al proyecto,
    como 'backend/config/prompt_base.txt'.
    """
    # Base: raíz del proyecto (sube 3 niveles desde /backend/utils/)
    ruta_base = Path(__file__).resolve().parent.parent.parent
    ruta_absoluta = ruta_base / ruta_relativa

    with open(ruta_absoluta, "r", encoding="utf-8") as archivo:
        return archivo.read()


def formatear_prompt(plantilla: str, datos: dict) -> str:
    """
    Inserta variables dentro de la plantilla de prompt de forma segura.
    
    Si faltan claves en el diccionario, deja el marcador tal cual.

    Ejemplo: "Hola {nombre}" con {"edad": 7} -> "Hola {nombre}"

    Retorna:
    - str: Prompt formateado
    """
    class SafeFormatter(dict):
        def __missing__(self, key):
            return "{" + key + "}"  # No lanza error si falta un dato

    return plantilla.format_map(SafeFormatter(datos))
