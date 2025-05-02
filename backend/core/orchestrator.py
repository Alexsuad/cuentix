# core/orchestrator.py

import threading
from tasks.generate_story import generate_story

def start_story_generation(story_id, data):
    """
    Inicia la generación de una historia de manera asíncrona.
    Lanza un hilo para no bloquear la API.
    
    Args:
        story_id (str): ID único de la historia.
        data (dict): Datos enviados desde el wizard.
    """

    def background_task():
        generate_story(story_id, data)

    # Lanzamos la tarea en segundo plano usando un hilo
    thread = threading.Thread(target=background_task)
    thread.start()
