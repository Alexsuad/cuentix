# core/apis/deepseek_api.py
# Este módulo gestiona la comunicación con la API de DeepSeek para generar texto a partir de un prompt.
# Implementa reintentos con tenacity, validación de claves y control de errores comunes (429, 503).

import requests
from config.settings import settings
from utils.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = get_logger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def generar_texto_desde_deepseek(prompt: str) -> str:
    """
    Envía un prompt a la API de DeepSeek para generar texto de IA.

    Parámetros:
    - prompt (str): Instrucción que describe el contenido deseado.

    Retorna:
    - str: Texto generado por DeepSeek, o mensaje de error si falla.
    """
    try:
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        logger.info("🧠 Enviando prompt a DeepSeek...")
        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data, timeout=30)
        response.raise_for_status()

        texto_generado = response.json()["choices"][0]["message"]["content"]
        logger.info("✅ Texto recibido correctamente desde DeepSeek.")
        return texto_generado

    except requests.HTTPError as e:
        if e.response.status_code == 429:
            logger.warning("⚠️ Límite de tasa excedido (429) en DeepSeek. Reintentando...")
        elif e.response.status_code == 503:
            logger.warning("⏳ Servicio temporalmente no disponible (503) en DeepSeek.")
        else:
            logger.error(f"❌ Error HTTP en DeepSeek: {e.response.status_code}")
        raise

    except Exception as e:
        logger.error(f"❌ Error inesperado al conectar con DeepSeek: {str(e)}")
        return "Lo siento, no pude generar el texto en este momento."
