# core/processors/image_generator.py

import os
import requests
from pathlib import Path
from config.settings import settings
from openai import OpenAI
from utils.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import openai

logger = get_logger(__name__)

class ImageGenerator:
    def __init__(self):
        # Inicializa el cliente de OpenAI con la clave API definida en settings
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    @retry(
        stop=stop_after_attempt(3),  # Reintenta hasta 3 veces en caso de error
        wait=wait_exponential(multiplier=2, min=5, max=30),  # Espera exponencial
        retry=retry_if_exception_type(openai.APIError)  # Solo reintenta si ocurre un APIError
    )
    def generate_image(self, texto: str, ruta_salida: str) -> str:
        try:
            # Crea el directorio destino si no existe
            ruta = Path(ruta_salida)
            ruta.parent.mkdir(parents=True, exist_ok=True)

            logger.info("🖼️ Enviando texto a la API de imagen para generar ilustración...")

            # Llamada a la API de OpenAI para generar la imagen
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=texto,
                n=1,
                size="1024x1024",
                timeout=60  # Tiempo de espera extendido para dar margen de respuesta
            )

            # Obtiene la URL de la imagen generada
            image_url = response.data[0].url
            logger.info(f"📅 Descargando imagen desde URL: {image_url}")

            # Descarga el contenido binario de la imagen
            img_data = requests.get(image_url, timeout=30).content

            # Guarda la imagen en disco
            with open(ruta, "wb") as handler:
                handler.write(img_data)

            logger.info(f"✅ Imagen generada correctamente en: {ruta}")
            return str(ruta)

        except Exception as e:
            # Registra el tipo de error para mejor trazabilidad
            error_type = type(e).__name__
            logger.error(f"❌ Error ({error_type}) al generar imagen para texto '{texto[:60]}...': {e}")
            return ""
