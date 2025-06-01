# ──────────────────────────────────────────────────────────────────────────────
# File: backend/core/processors/text_generator.py
# Descripción: Genera el texto del cuento utilizando un modelo de lenguaje (DeepSeek).
# Incluye manejo de errores, reintentos y carga portable de plantillas.
# ──────────────────────────────────────────────────────────────────────────────

import requests  # Para realizar peticiones HTTP a la API de DeepSeek
import urllib3  # Para desactivar advertencias SSL en entorno de pruebas
import re  # Para dividir el texto del cuento en escenas
from config.settings import settings  # Configuración global del proyecto
from utils.prompts import cargar_plantilla_prompt, formatear_prompt  # Carga y formato de prompt
from utils.logger import get_logger  # Logger del sistema
from typing import List, Tuple  # Tipado para listas de escenas

# Inicializar logger para este módulo
logger = get_logger(__name__)

# Desactiva advertencias SSL solo si DEBUG=True (modo desarrollo en WSL)
if settings.DEBUG:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TextGenerator:
    """
    Clase que encapsula la lógica para generar el texto de un video-cuento infantil
    utilizando el modelo DeepSeek Chat v2. Usa una plantilla base personalizada.
    """

    def __init__(self):
        # Clave de API y endpoint oficial de DeepSeek (por dominio, no IP)
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = "https://api.deepseek.ai/v1/chat/completions"

    def generate_text(self, datos_usuario: dict) -> str:
        """
        Genera el cuento completo usando la API de DeepSeek y los datos del usuario.

        Args:
            datos_usuario (dict): Diccionario con datos para el cuento.

        Returns:
            str: Cuento generado o cadena vacía si hubo error.
        """

        # Validar que no falte ningún dato clave en el prompt
        campos_requeridos = [
            "nombre", "edad", "personaje_principal",
            "lugar", "villano", "objeto_magico", "tipo_final"
        ]
        for campo in campos_requeridos:
            if campo not in datos_usuario:
                logger.error(f"❌ Campo faltante en datos_usuario: {campo}")
                return ""

        # Cargar la plantilla y preparar el prompt completo
        try:
            plantilla = cargar_plantilla_prompt(settings.PROMPT_TEMPLATE_PATH)
        except FileNotFoundError:
            logger.error("❌ Archivo de plantilla no encontrado.")
            return ""
        except Exception as e:
            logger.error(f"❌ Error al cargar plantilla: {e}")
            return ""

        prompt = formatear_prompt(plantilla, datos_usuario)
        logger.info("🧠 Enviando prompt a DeepSeek (modo seguro)...")

        # Armar solicitud HTTP
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat-v2",
            "messages": [
                {"role": "system", "content": "Eres un experto en cuentos infantiles."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 1000
        }

        # Enviar solicitud
        try:
            response = requests.post(
                url=self.api_url,
                headers=headers,
                json=data,
                timeout=30,
                verify=not settings.DEBUG  # Solo desactiva SSL en modo DEBUG
            )
            response.raise_for_status()
            cuento = response.json()["choices"][0]["message"]["content"].strip()
            logger.info("✅ Cuento generado correctamente.")
            return cuento

        except Exception as e:
            logger.error(f"❌ Error en la generación de texto con DeepSeek: {e}")
            return ""

    def dividir_en_escenas(self, cuento: str) -> List[Tuple[str, str]]:
        """
        Divide el cuento en escenas usando etiquetas como [Intro], [Conflicto], etc.

        Args:
            cuento (str): Texto completo del cuento.

        Returns:
            List[Tuple[str, str]]: Lista de escenas con su tipo.
        """
        partes = re.split(r"\[(Intro|Conflicto|Resolucion|Moraleja)\]", cuento)
        etiquetas_y_texto = list(zip(partes[1::2], partes[2::2]))
        return [(etq, txt.strip()) for etq, txt in etiquetas_y_texto if txt.strip()]
