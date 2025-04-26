# archivo: utils/helpers.py

import os
import re
import uuid
import base64

def limpiar_texto(texto: str) -> str:
    """
    Elimina caracteres especiales, saltos de línea innecesarios
    y deja el texto limpio para usar en prompts o archivos.
    """
    texto = texto.replace("\n", " ")               # Elimina saltos de línea
    texto = re.sub(r'\s+', ' ', texto)             # Reemplaza múltiples espacios por uno
    texto = texto.strip()                          # Elimina espacios al principio y final
    return texto


def generar_id_unico() -> str:
    """
    Genera un ID único (UUID) para nombrar archivos sin colisiones.
    """
    return str(uuid.uuid4())


def convertir_base64_a_imagen(base64_data: str, output_path: str) -> None:
    """
    Convierte una imagen codificada en Base64 a un archivo .png o .jpg.

    :param base64_data: Cadena base64 de la imagen
    :param output_path: Ruta donde se guardará el archivo de imagen
    """
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(base64_data))
