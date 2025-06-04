# core/orchestrator.py
# Ejecuta el pipeline de generación de cuento en segundo plano (hilo)

import threading
from core.orchestrators.story_pipeline import run_pipeline  # ← nuevo import

def start_story_generation(story_id, data):
    """
    Inicia la generación de una historia de manera asíncrona.
    Lanza un hilo para no bloquear la API.
    """

    def background_task():
        # Ejecuta el pipeline completo en segundo plano
        run_pipeline(story_id, data)     # ← llama al nuevo pipeline

    # Lanzamos la tarea en segundo plano usando un hilo
    thread = threading.Thread(target=background_task)
    thread.start()
