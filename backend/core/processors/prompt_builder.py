# core/processors/prompt_builder.py

"""
Este módulo se encarga de construir dinámicamente prompts personalizados 
a partir de los parámetros que el niño o niña selecciona desde el frontend.
La salida es una cadena de texto que se combina con el prompt global para 
generar una historia única y adaptada.
"""

def construir_prompt_personalizado(params: dict) -> str:
    """
    Recibe un diccionario con datos seleccionados por el niño/a y arma un prompt específico.

    Parámetros esperados en el diccionario:
    - nombre: Nombre del protagonista
    - edad: Edad del niño
    - rol: Rol del protagonista (explorador, astronauta, dragón, etc.)
    - lugar: Escenario donde sucede el cuento
    - objeto: Objeto mágico o especial
    - desafio: Desafío o conflicto a resolver
    - criatura: Personaje mágico o animal secundario
    - color: Color favorito del niño
    - final: Tipo de final (feliz, sorpresa, aprendizaje, etc.)

    Retorna:
    - prompt (str): Prompt personalizado, listo para combinar con el prompt global.
    """
    # Recuperamos los datos desde el diccionario (usando valores por defecto si faltan)
    nombre = params.get("nombre", "Tomi")
    edad = params.get("edad", "5")
    rol = params.get("rol", "explorador")
    compañero = params.get("compañero", "un dragón azul")
    lugar = params.get("lugar", "una isla flotante")
    objeto = params.get("objeto", "una lupa mágica")
    desafio = params.get("desafio", "rescatar a un amigo perdido")
    criatura = params.get("criatura", "un unicornio")
    color = params.get("color", "verde")
    final = params.get("final", "feliz")

    # Construimos el prompt personalizado
    prompt = (
        f"El protagonista es un {rol} llamado {nombre}, que tiene {edad} años. "
        f"Está acompañado por {compañero} en una aventura en {lugar}. "
        f"Encuentra un objeto especial: {objeto}. "
        f"Su misión es {desafio}, enfrentando desafíos con la ayuda de una criatura como {criatura}. "
        f"El color favorito del protagonista es {color}, y el cuento debe terminar con un final {final}."
    )

    return prompt
