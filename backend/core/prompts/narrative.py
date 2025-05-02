# core/prompts/narrative.py
# Genera el prompt narrativo base para el modelo de texto (DeepSeek, GPT, etc.)

def build_narrative_prompt(data):
    """
    Construye un prompt narrativo a partir de los datos enviados por el Wizard.
    
    Args:
        data (dict): Diccionario con las elecciones del usuario.
    
    Returns:
        str: Prompt listo para enviar al modelo de texto.
    """
    nombre = data.get("nombre", "un niño o niña")
    edad = data.get("edad", "5")
    personaje = data.get("personaje_principal", "un personaje principal")
    lugar = data.get("lugar", "un lugar mágico")
    objeto = data.get("objeto_magico", "un objeto mágico")
    villano = data.get("villano", "un villano")
    tipo_final = data.get("tipo_final", "feliz")

    prompt = (
        f"Crea un cuento para un niño o niña de {edad} años llamado {nombre}. "
        f"El personaje principal será {personaje}, quien vive en {lugar}. "
        f"Durante la historia encontrará {objeto}, que le ayudará a enfrentarse a {villano}. "
        f"El final debe ser {tipo_final}, y el cuento debe tener un mensaje positivo, "
        f"ser divertido, fácil de entender y adecuado para la edad del niño o niña."
    )

    return prompt
