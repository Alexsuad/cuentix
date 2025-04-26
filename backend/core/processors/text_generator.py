# core/processors/text_generator.py

# Este módulo genera un cuento infantil personalizado a partir de una plantilla de prompt.
# Utiliza una IA de lenguaje (como DeepSeek o GPT) y datos proporcionados por el usuario (niño o niña).

import os
from config.settings import settings
from utils.prompts import cargar_plantilla_prompt, formatear_prompt  # ✅ ESTA SÍ
from utils.logger import get_logger
from openai import OpenAI
from typing import Optional


plantilla = cargar_plantilla_prompt("config/prompt_base.txt")


logger = get_logger(__name__)

class TextGenerator:
    def __init__(self):
        # Cliente de OpenAI para generación de texto (usa API Key y Project ID si aplica)
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            organization=settings.OPENAI_ORG_ID if hasattr(settings, "OPENAI_ORG_ID") else None,
            project=settings.OPENAI_PROJECT_ID if hasattr(settings, "OPENAI_PROJECT_ID") else None
        )

    def generar_cuento(self, datos_usuario: dict) -> str:
        """
        Genera un cuento infantil basado en los datos del niño/a usando una plantilla de prompt.
        """
        # Paso 0: Validar campos obligatorios
        campos_requeridos = [
            "nombre", "edad", "personaje_principal", "lugar",
            "villano", "objeto_magico", "tipo_final"
        ]
        for campo in campos_requeridos:
            if campo not in datos_usuario:
                logger.error(f"❌ Campo faltante: {campo}")
                return ""

        # Paso 1: Cargar plantilla base desde archivo
        try:
            plantilla = cargar_plantilla_prompt("config/prompt_base.txt")
        except FileNotFoundError:
            logger.error("❌ Archivo de plantilla no encontrado")
            return ""

        # Paso 2: Insertar variables del usuario en la plantilla
        prompt_formateado = formatear_prompt(plantilla, datos_usuario)

        # Paso 3: Enviar a modelo para generar texto
        try:
            logger.info("🧠 Solicitando historia al modelo de lenguaje...")
            respuesta = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres un experto en cuentos infantiles."},
                    {"role": "user", "content": prompt_formateado}
                ],
                temperature=0.8,
                max_tokens=800
            )
            cuento = respuesta.choices[0].message.content.strip()
            logger.info("✅ Cuento generado correctamente.")
            return cuento

        except Exception as e:
            logger.error(f"❌ Error al generar cuento: {e}")
            return ""

    def dividir_en_escenas(self, cuento: str) -> list:
        """
        Divide un cuento largo en escenas usando etiquetas [Intro], [Conflicto], etc.
        """
        import re
        escenas = re.split(r"\[(Intro|Conflicto|Resolucion|Moraleja)\]", cuento)
        return [esc.strip() for esc in escenas if esc.strip()]
