# core/processors/image_generator.py

import os
from pathlib import Path
from config.settings import settings
from openai import OpenAI
from utils.logger import get_logger

logger = get_logger(__name__)

class ImageGenerator:
    def __init__(self):
        # Solo usar api_key, sin project_id
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def generate_image(self, texto: str, ruta_salida: str) -> str:
        try:
            ruta = Path(ruta_salida)
            ruta.parent.mkdir(parents=True, exist_ok=True)

            logger.info("🖼️ Enviando texto a la API de imagen para generar ilustración...")
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=texto,
                n=1,
                size="1024x1024"
            )

            image_url = response.data[0].url
            logger.info(f"📥 Descargando imagen desde URL: {image_url}")

            import requests
            img_data = requests.get(image_url).content
            with open(ruta_salida, "wb") as handler:
                handler.write(img_data)

            if not ruta.exists():
                raise FileNotFoundError(f"La imagen no se guardó en {ruta_salida}")

            logger.info(f"✅ Imagen generada correctamente en: {ruta_salida}")
            return str(ruta_salida)

        except Exception as e:
            logger.error(f"❌ Error al generar imagen: {e}")
            return ""
