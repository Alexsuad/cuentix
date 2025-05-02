# test_openai_api_simple.py
# Verifica si OpenAI API Key y Proyecto funcionan con generación de imagen

import openai
import logging
from dotenv import load_dotenv
import os

# Cargar claves desde .env
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Asignar clave de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def probar_openai_image():
    try:
        logger.info("🎨 Enviando solicitud de generación de imagen (modo nuevo)...")

        response = openai.images.generate(
            model="dall-e-3",
            prompt="Un dragón sonriente volando sobre un castillo en el cielo",
            n=1,
            size="1024x1024"
        )

        url = response.data[0].url
        logger.info(f"✅ Imagen generada correctamente: {url}")

    except Exception as e:
        logger.error(f"❌ Error al generar imagen con OpenAI: {e}")

if __name__ == "__main__":
    probar_openai_image()
