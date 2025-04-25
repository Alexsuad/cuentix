# utils/prompts.py

# Este módulo gestiona la carga y formateo seguro de los prompts de texto para Cuentix.

import os

def cargar_plantilla_prompt(ruta: str) -> str:
    """
    Carga el contenido de una plantilla de prompt desde un archivo de texto.
    
    Parámetros:
    - ruta (str): Ruta relativa del archivo (por ejemplo: 'config/prompt_base.txt')
    
    Retorna:
    - str: Contenido del archivo como string.
    """
    ruta_absoluta = os.path.abspath(ruta)  # Convierte la ruta relativa en absoluta
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
