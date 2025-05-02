# tasks/generate_story.py

from models.models import Story
from core.prompts.narrative import build_narrative_prompt

import os

# Simulación de base de datos en memoria (importamos STORIES_DB para guardar estados)
from utils.db_memory import STORIES_DB 

def generate_story(story_id, data):
    """
    Función que genera el video cuento completo basado en las elecciones del wizard.

    Args:
        story_id (str): ID único de la historia.
        data (dict): Datos enviados desde el wizard (elecciones).
    """

    try:
        print(f"🚀 Iniciando generación de historia {story_id}")

        # 1. Actualizar estado a "generating"
        story = STORIES_DB.get(story_id)
        if story:
            story.update_status("generating")

        # 2. Construir prompt narrativo
        narrative_prompt = build_narrative_prompt(data)
        print(f"📖 Prompt construido:\n{narrative_prompt}")

        # 3. (AQUÍ IRÁ) Llamar a IA de texto → generar historia completa
        # historia_texto = llamar_ia_para_texto(narrative_prompt)

        # 4. (AQUÍ IRÁ) Dividir en escenas

        # 5. (AQUÍ IRÁ) Generar imágenes

        # 6. (AQUÍ IRÁ) Generar audios

        # 7. (AQUÍ IRÁ) Generar subtítulos

        # 8. (AQUÍ IRÁ) Montar video final con MoviePy

        # 9. Actualizar estado a "completed" (provisionalmente simulamos éxito)
        if story:
            fake_video_path = os.path.abspath("assets/videos/demo_video.mp4")  # RUTA DE EJEMPLO
            story.update_status("completed", video_path=fake_video_path)

        print(f"✅ Historia {story_id} generada exitosamente.")

    except Exception as e:
        print(f"❌ Error al generar historia {story_id}: {str(e)}")
        if story:
            story.update_status("failed")

