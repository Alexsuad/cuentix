# utils/openai_tools.py

import openai
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

def verificar_openai():
    """
    Verifica si la clave API de OpenAI está activa y puede acceder a los modelos.
    Ideal para confirmar conectividad antes de usar DALL·E o TTS.
    """
    try:
        openai.api_key = settings.OPENAI_API_KEY
        modelos = openai.models.list()
        logger.info("✅ Conexión exitosa con OpenAI. Modelos disponibles:")
        for modelo in modelos.data[:5]:
            logger.info(f" - {modelo.id}")
        return True
    except Exception as e:
        logger.error(f"❌ No se pudo conectar con OpenAI: {str(e)}")
        return False
