# ──────────────────────────────────────────────────────────────────────────────
# File: core/processors/prompt_builder.py
# Descripción: Construye un prompt personalizado a partir de los datos enviados
# desde el frontend, adaptado a los gustos del niño o niña. Este prompt será
# utilizado por el generador de texto para crear una historia infantil única.
# ──────────────────────────────────────────────────────────────────────────────

# ╭─────────────────────────────── Importaciones ───────────────────────────────╮

from core.validators.campos_requeridos import CAMPOS_REQUERIDOS  # Lista centralizada de campos requeridos

# ╰─────────────────────────────────────────────────────────────────────────────╯


# ───────────────────────────── Construcción del Prompt ────────────────────────

def construir_prompt_personalizado(params: dict) -> str:
    """
    Genera un prompt narrativo infantil usando los datos proporcionados por el usuario.

    Args:
        params (dict): Diccionario con los campos seleccionados en el frontend.

    Returns:
        str: Prompt listo para ser enviado al modelo de IA generativa.
    """

    # Obtener valores desde el diccionario con valores por defecto si faltan
    nombre = params.get("nombre", "Alex")
    edad = params.get("edad", 5)
    personaje_principal = params.get("personaje_principal", "un dragón curioso")
    lugar = params.get("lugar", "el bosque encantado")
    villano = params.get("villano", "el ogro gruñón")
    objeto_magico = params.get("objeto_magico", "una brújula brillante")
    tipo_final = params.get("tipo_final", "feliz")

    # Crear el prompt final usando una estructura narrativa coherente
    prompt = (
        f"El cuento es para un niño llamado {nombre}, de {edad} años. "
        f"El personaje principal es {personaje_principal}, que vive una aventura en {lugar}. "
        f"En el camino se enfrentará al villano {villano}, pero contará con la ayuda de "
        f"un objeto mágico muy especial: {objeto_magico}. "
        f"La historia debe terminar con un final {tipo_final}, adaptado a su edad y estilo."
    )

    return prompt
