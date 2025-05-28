# core/processors/text_generator.py

from config.settings import settings
from utils.prompts import cargar_plantilla_prompt, formatear_prompt
from utils.logger import get_logger
from openai import OpenAI
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import openai

logger = get_logger(__name__)

class TextGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(openai.RateLimitError)
    )
    def generar_cuento(self, datos_usuario: dict) -> str:
        campos_requeridos = [
            "nombre", "edad", "personaje_principal", "lugar",
            "villano", "objeto_magico", "tipo_final"
        ]
        for campo in campos_requeridos:
            if campo not in datos_usuario:
                logger.error(f"❌ Campo faltante: {campo}")
                return ""

        try:
            plantilla = cargar_plantilla_prompt("backend/config/prompt_base.txt")
        except FileNotFoundError:
            logger.error("❌ Archivo de plantilla no encontrado")
            return ""

        prompt_formateado = formatear_prompt(plantilla, datos_usuario)

        try:
            logger.info("🧠 Solicitando historia al modelo de lenguaje...")

            respuesta = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres un experto en cuentos infantiles."},
                    {"role": "user", "content": prompt_formateado}
                ],
                temperature=0.8,
                max_tokens=800,
                timeout=60  # ⏱️ Extiende el tiempo de espera (por defecto suele ser 10s)
            )

            cuento = respuesta.choices[0].message.content.strip()
            logger.info("✅ Cuento generado correctamente.")
            return cuento

        except Exception as e:
            logger.error(f"❌ Error al generar cuento: {e}")
            return ""

    def dividir_en_escenas(self, cuento: str) -> list:
        import re
        escenas = re.split(r"\[(Intro|Conflicto|Resolucion|Moraleja)\]", cuento)
        return [esc.strip() for esc in escenas if esc.strip()]
