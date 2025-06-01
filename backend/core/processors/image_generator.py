# ────────────────────────────────────────────────────────────────────────
# File: backend/core/processors/image_generator.py
# Descripción: Genera imágenes utilizando la API de OpenAI (DALL·E).
# Incluye normalización del prompt, reintentos, y un modo fallback con imagen placeholder.
# ────────────────────────────────────────────────────────────────────────

import os
import requests
import shutil
from pathlib import Path
from config.settings import settings
from openai import OpenAI, BadRequestError, APIError, RateLimitError, AuthenticationError, NotFoundError, PermissionDeniedError, InternalServerError
from utils.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = get_logger(__name__)

PLACEHOLDER_IMAGE_PATH = Path(settings.PROJECT_ROOT) / "frontend" / "assets" / "img" / "placeholder_cuentix.png"

class ImageGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=5, max=30),
        retry=retry_if_exception_type((APIError, RateLimitError)),
        before_sleep=lambda s: logger.warning(
            f"🔁 Reintentando generación de imagen (intento #{s.attempt_number}). Error: {s.outcome.exception()}"
        )
    )
    def generate_image(self, texto: str, ruta_salida: str) -> str:
        try:
            prompt = texto[:900]
            prompt_limpio = prompt.encode("ascii", "ignore").decode()
            prompt_final = (
                "Claymation digital 3D illustration for children: "
                f"{prompt_limpio}, pastel colors, soft shadows, round shapes, expressive faces, Pixar-like style"
            )
            logger.debug(f"📨 Prompt enviado a DALL·E: {prompt_final!r}")
            ruta = Path(ruta_salida)
            ruta.parent.mkdir(parents=True, exist_ok=True)
            logger.info("🖼️ Enviando texto a la API de imagen para generar ilustración...")

            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt_final,
                size="1024x1024",
                n=1,
                style="natural"
            )

            image_url = response.data[0].url
            logger.info(f"📅 Descargando imagen desde URL: {image_url}")
            img_data = requests.get(image_url, timeout=30).content
            with open(ruta, "wb") as handler:
                handler.write(img_data)

            logger.info(f"✅ Imagen generada correctamente en: {ruta}")
            return str(ruta)

        except BadRequestError as e:
            logger.error(f"❌ DALL·E BadRequestError (400): {e.response.json() if e.response else e}")
            pass

        except (APIError, RateLimitError) as e:
            logger.error(f"❌ DALL·E API/RateLimit (después de reintentos): {e}")
            pass

        except Exception as e:
            error_type = type(e).__name__
            logger.error(f"❌ Error ({error_type}) inesperado durante la generación de imagen para texto '{texto[:60]}...': {e}")
            pass

        logger.warning("⚠️ Generación de imagen principal fallida. Intentando usar imagen placeholder...")
        try:
            if PLACEHOLDER_IMAGE_PATH.exists():
                shutil.copy(PLACEHOLDER_IMAGE_PATH, ruta_salida)
                logger.info(f"🖼️ Imagen placeholder copiada a: {ruta_salida}")
                return str(ruta_salida)
            else:
                logger.error(f"❌ Imagen placeholder no encontrada en: {PLACEHOLDER_IMAGE_PATH}. No se puede usar fallback.")
                return ""
        except Exception as copy_e:
            logger.error(f"❌ Error al copiar imagen placeholder: {copy_e}")
            return ""
