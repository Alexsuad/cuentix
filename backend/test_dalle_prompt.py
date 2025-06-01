# backend/test_dalle_prompt.py
# ──────────────────────────────────────────────────────────────────────────────
# Propósito: Script de prueba aislado para verificar la generación de imágenes
#            con la API de OpenAI (DALL·E), usando un prompt específico.
# ──────────────────────────────────────────────────────────────────────────────

import os
import sys
from pathlib import Path

# Ajustar sys.path para importar desde backend (si se ejecuta desde la raíz)
# Si ejecutas desde backend/, esta parte podría no ser necesaria
try:
    backend_dir = str(Path(__file__).resolve().parents[1])
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
except IndexError: # Se ejecuta desde la raíz del proyecto
    sys.path.insert(0, str(Path.cwd() / "backend"))


from dotenv import load_dotenv
from openai import OpenAI, BadRequestError
from config.settings import settings # Usar tu configuración centralizada
from utils.logger import get_logger

logger = get_logger(__name__)

# Cargar variables de entorno (aunque settings ya lo hace, es bueno para un script aislado)
# Asume que .env está en la carpeta backend/
dotenv_path = Path(__file__).resolve().parent / ".env" # Usar BACKEND_DIR de settings
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    logger.warning(f"⚠️  Archivo .env no encontrado en: {dotenv_path}")


def test_dalle_prompt(prompt_texto: str):
    """
    Intenta generar una imagen usando DALL-E con el prompt proporcionado.

    Args:
        prompt_texto (str): El texto a usar como prompt para DALL·E.
    """
    try:
        # Utilizar la clave API cargada por settings
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Normalización básica del prompt (puedes refinarla aquí)
        prompt_limpio = prompt_texto[:900] # Limitar a 900 caracteres (DALL-E 3 tiene límite de 1000)
        prompt_limpio = prompt_limpio.encode("ascii", "ignore").decode()

        # Estilo visual estándar de Cuentix (opcional, puedes probar sin él)
        prompt_final = (
            "Claymation digital 3D illustration for children: "
            f"{prompt_limpio}, pastel colors, soft shadows, round shapes, expressive faces, Pixar-like style"
        )
        # O prueba solo con el prompt limpio:
        # prompt_final = prompt_limpio

        logger.info(f"🔍 Enviando prompt a DALL·E:\n{prompt_final!r}")

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_final,
            size="1024x1024",
            n=1
        )

        image_url = response.data[0].url
        logger.info(f"✅ Imagen generada correctamente. URL: {image_url}")
        print(f"\n🟢 IMAGEN GENERADA CON ÉXITO:")
        print(f"   URL: {image_url}")

    except BadRequestError as e:
        logger.error(f"❌ DALL·E BadRequestError (400): {e.response.json() if e.response else e}")
        print(f"\n🔴 ERROR BAD REQUEST (400):")
        print(f"   Detalle: {e.response.json() if e.response else e}")
    except Exception as e:
        error_type = type(e).__name__
        logger.error(f"❌ Error inesperado ({error_type}) al generar imagen: {e}")
        print(f"\n🔴 ERROR INESPERADO ({error_type}):")
        print(f"   Detalle: {e}")


if __name__ == "__main__":
    # ──────────────────────────────────────────────────────────────────────────
    # MODIFICA ESTE PROMPT CON EL TEXTO EXACTO QUE ESTÁ FALLANDO
    # EN TU SCRIPT video_generator_test.py O main_mvp_audio_unico.py
    # ──────────────────────────────────────────────────────────────────────────
    prompt_problematico = "perro jugando en la playa"
    # O el prompt de la hada Luna:
    # prompt_problematico = "Luna era una hada con alas de cristal. Vivía en una nube donde llovían caramelos."
    # O un prompt muy simple para verificar la conexión:
    # prompt_problematico = "A red apple on a table"

    test_dalle_prompt(prompt_problematico)