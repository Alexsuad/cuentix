# ──────────────────────────────────────────────────────────────────────────────
# File: core/processors/text_generator.py
# Descripción: Genera el texto del cuento utilizando un modelo de lenguaje (DeepSeek).
# Incluye manejo de errores, validación de campos y segmentación en escenas.
# ──────────────────────────────────────────────────────────────────────────────

# ╭─────────────────────────────── Importaciones ───────────────────────────────╮
import socket                             # Para verificar resolución DNS
import requests                           # Peticiones HTTP hacia la API de DeepSeek
import urllib3                            # Desactiva advertencias SSL en modo DEBUG
import re                                 # Expresiones regulares para dividir escenas
from typing import List, Tuple            # Tipado de listas y tuplas

from config.settings import settings      # Configuración general desde .env
from utils.logger import get_logger       # Sistema de logging del backend
from core.validators.campos_requeridos import CAMPOS_REQUERIDOS  # Campos requeridos
from core.processors.prompt_builder import construir_prompt_personalizado  # Prompt dinámico
# ╰─────────────────────────────────────────────────────────────────────────────╯

# ───────────────────────────── Inicialización global ──────────────────────────

logger = get_logger(__name__)

if settings.DEBUG:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ───────────────────────────── Clase Principal ────────────────────────────────

class TextGenerator:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.model = getattr(settings, "DEEPSEEK_MODEL", "deepseek-chat")

        # Verificar si el dominio .ai se resuelve correctamente
        try:
            socket.gethostbyname("api.deepseek.ai")
            self.api_url = "https://api.deepseek.ai/v1/chat/completions"
            logger.info("🌐 DeepSeek: DNS correcto (.ai)")
        except socket.gaierror:
            self.api_url = "https://api.deepseek.com/v1/chat/completions"
            logger.warning("⚠️ DeepSeek: usando fallback .com por fallo DNS")

    def generar_cuento(self, datos_usuario: dict) -> Tuple[str, List[str]]:
        """
        Genera el cuento completo y lo divide en escenas.

        Parámetros:
        - datos_usuario (dict): Diccionario con los campos del frontend.

        Retorna:
        - Tuple[str, List[str]]: Texto completo del cuento y lista de escenas.
        """

        # Validar que estén presentes todos los campos necesarios
        for campo in CAMPOS_REQUERIDOS:
            if campo not in datos_usuario:
                logger.error(f"❌ Campo faltante en datos_usuario: {campo}")
                return "", []

        # Construir el prompt narrativo desde el generador de plantillas
        try:
            prompt = construir_prompt_personalizado(datos_usuario)
        except Exception as e:
            logger.error(f"❌ Error al construir prompt personalizado: {e}")
            return "", []

        logger.info("🧠 Enviando prompt a DeepSeek (modo seguro)...")
        logger.debug(f"📤 Prompt enviado:\n{prompt}")

        # Definir headers y payload según formato DeepSeek actualizado
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Eres un experto en cuentos infantiles."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 1000
        }

        # Hacer la petición y procesar respuesta
        try:
            response = requests.post(
                url=self.api_url,
                headers=headers,
                json=data,
                timeout=30,
                verify=not settings.DEBUG
            )
            response.raise_for_status()
            resultado = response.json()
            cuento = resultado["choices"][0]["message"]["content"].strip()
            logger.info("✅ Cuento generado correctamente.")
            logger.debug(f"📘 Cuento generado:\n{cuento}")
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error en la generación de texto con DeepSeek: {e}")
            if hasattr(e, "response") and e.response is not None:
                logger.error(f"📨 Respuesta del servidor:\n{e.response.text}")
            return "", []

        # Limpiar y segmentar el cuento
        cuento = self.limpiar_texto(cuento)
        escenas = self.dividir_en_escenas(cuento)

        # ─── Fallback en caso de que no haya escenas ───────────────────────────
        if not escenas:
            logger.warning("⚠️ No se encontraron etiquetas [Intro], [Conflicto]... Probando con doble salto de línea.")
            escenas = [s.strip() for s in cuento.split("\n\n") if s.strip()]

        if not escenas:
            logger.warning("⚠️ Texto sin saltos dobles. Usando el texto completo como única escena.")
            escenas = [cuento.strip()]

        logger.info(f"📑 Escenas detectadas: {len(escenas)}")
        return cuento, escenas

    def dividir_en_escenas(self, cuento: str) -> List[str]:
        """
        Divide el cuento en escenas usando etiquetas predefinidas.

        Parámetros:
        - cuento (str): Texto completo generado.

        Retorna:
        - List[str]: Lista de escenas como strings.
        """
        partes = re.split(r"\[(Intro|Conflicto|Resolucion|Moraleja)\]", cuento)
        etiquetas_y_texto = list(zip(partes[1::2], partes[2::2]))
        return [txt.strip() for _, txt in etiquetas_y_texto if txt.strip()]

    def limpiar_texto(self, texto: str) -> str:
        """
        Limpia símbolos escritos como palabras (comillas, guión, etc.)
        que interfieren con TTS o subtítulos.

        Parámetros:
        - texto (str): Texto original.

        Retorna:
        - str: Texto limpio.
        """
        texto = texto.replace("comillas", "\"")
        texto = texto.replace("asterisco", "*")
        texto = texto.replace("guión", "-")
        return texto.strip()

# ──────────────────────────────────────────────────────────────────────────────
