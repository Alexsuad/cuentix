#──────────────────────────────────────────────────────────────────────────────
# File: backend/utils/prompts.py
# Descripción: Utilidades para trabajar con plantillas de prompt en Cuentix.
# Incluye carga de plantillas desde archivos y formateo seguro con datos.
# ──────────────────────────────────────────────────────────────────────────────

from pathlib import Path
from typing import Union # Importar Union para el tipado de ruta

# ────────────────────────────────────────────────────────────────────
# Función: cargar_plantilla_prompt
# Propósito: Cargar archivo de texto (prompt) desde ruta
# ────────────────────────────────────────────────────────────────────
def cargar_plantilla_prompt(ruta: Union[str, Path]) -> str:
    """
    Carga una plantilla desde una ruta absoluta o relativa (resuelta automáticamente).

    Args:
        ruta (Union[str, Path]): Ruta absoluta o relativa al archivo de plantilla.

    Returns:
        str: Contenido de la plantilla como string.

    Raises:
        FileNotFoundError: Si la plantilla no se encuentra.
    """
    # Convertir a Path y obtener ruta absoluta, resolviendo ~ y rutas relativas
    ruta_absoluta = Path(ruta).expanduser().resolve()

    # Verificar existencia
    if not ruta_absoluta.exists():
        raise FileNotFoundError(f"❌ Plantilla no encontrada en: {ruta_absoluta}")

    # Leer contenido como string con codificación UTF-8
    return ruta_absoluta.read_text(encoding="utf-8")


# ────────────────────────────────────────────────────────────────────
# Función: formatear_prompt
# Propósito: Insertar datos del usuario en la plantilla de forma segura
# ────────────────────────────────────────────────────────────────────
def formatear_prompt(plantilla: str, datos: dict) -> str:
    """
    Rellena una plantilla con los datos proporcionados de forma segura.

    Si falta un campo, se conserva el marcador tal cual (no lanza error).

    Args:
        plantilla (str): Texto base con llaves {campo}.
        datos (dict): Diccionario de datos para rellenar.

    Returns:
        str: Plantilla formateada con los valores disponibles.
    """
    class SafeFormatter(dict):
        def __missing__(self, key):
            return "{" + key + "}"  # Mantiene el marcador si falta

    return plantilla.format_map(SafeFormatter(datos))