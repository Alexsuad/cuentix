# config/prompts.py

"""
Este archivo contiene los prompts base (globales) que definen el estilo general
para cada módulo de IA utilizado en Cuentix.
Estos valores NO cambian por usuario y son comunes a todos los cuentos.
"""

# Prompt global para generación del cuento (usado por DeepSeek)
PROMPT_GLOBAL_TEXTO = (
    "Crea un cuento corto para niños de entre 4 y 6 años. El cuento debe tener un lenguaje claro, "
    "incluir un mensaje educativo y terminar con un final positivo. El estilo debe ser divertido, "
    "ligero, con personajes entrañables y aventuras emocionantes, pero apropiadas para su edad."
)

# Prompt base para la generación de imágenes (se combinará con el contenido de cada párrafo)
PROMPT_IMAGEN_ESTILO = (
    "Estilo ilustración infantil, libro de cuentos, colores vivos, sin texto, formato horizontal, "
    "alegre y amigable para niños."
)

# Parámetros por defecto para el modelo de voz (ElevenLabs)
PROMPT_AUDIO_ESTILO = {
    "voz_id": "21m00Tcm4TlvDq8ikWAM",     # Voz por defecto (Rachel)
    "stability": 0.5,                     # Estabilidad emocional de la voz
    "similarity_boost": 0.7              # Qué tanto se parece al estilo de la voz base
}
