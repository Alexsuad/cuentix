# backend/test_google_image_api.py
# ──────────────────────────────────────────────────────────────────────────────
# Propósito: Script de prueba aislado para verificar la generación de imágenes
#            con la API de Google Cloud Vertex AI (modelos Imagen o Gemini).
# ──────────────────────────────────────────────────────────────────────────────

import os
import sys
import base64 # Para decodificar imágenes base64
from io import BytesIO # Para manejar datos binarios de imagen en memoria
from pathlib import Path # Para manejo de rutas

# Ajustar sys.path para importar desde backend (si se ejecuta desde la raíz)
try:
    backend_dir = str(Path(__file__).resolve().parents[1])
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
except IndexError: # Se ejecuta desde la raíz del proyecto
    sys.path.insert(0, str(Path.cwd() / "backend"))


from dotenv import load_dotenv # Para cargar .env si settings no lo hace
from config.settings import settings # Usar tu configuración centralizada
from utils.logger import get_logger # Usar tu logger

# Importar librerías de Google Cloud
# Necesitarás instalarlas: pip install google-cloud-aiplatform Pillow protobuf
try:
    from google.cloud import aiplatform
    from google.cloud.aiplatform_v1beta1.types import (
        PredictRequest,
        PredictResponse,
        # Value, # Ya no es necesario importar Value si pasamos diccionarios directamente
    )
    from google.cloud.aiplatform_v1beta1.services import prediction_service
    from google.api_core.exceptions import GoogleAPIError # Excepción general de Google Cloud
    from PIL import Image # Para guardar la imagen (requiere Pillow)
    # from google.protobuf.struct_pb2 import Struct # Ya no es necesario importar Struct
    
    logger = get_logger(__name__)

except ImportError:
    logger = get_logger(__name__)
    logger.error("❌ Las librerías de Google Cloud no están instaladas. Instala: pip install google-cloud-aiplatform Pillow protobuf")
    sys.exit(1)
except Exception as e:
    logger = get_logger(__name__)
    logger.error(f"❌ Error al importar librerías de Google Cloud: {e}")
    sys.exit(1)


def test_google_image_generation(prompt_texto: str, output_path: str) -> bool:
    """
    Intenta generar una imagen usando Google Cloud Vertex AI (modelo Imagen)
    con el prompt proporcionado.

    Args:
        prompt_texto (str): El texto a usar como prompt para la generación.
        output_path (str): Ruta donde guardar la imagen generada.

    Returns:
        bool: True si la imagen se genera y guarda correctamente, False en caso de fallo.
    """
    try:
        logger.info("🔍 Inicializando cliente de Google Cloud Vertex AI...")
        # project_id y region se obtienen de settings
        project_id = settings.GOOGLE_CLOUD_PROJECT_ID
        region = settings.GOOGLE_CLOUD_REGION

        if not project_id:
             logger.error("❌ GOOGLE_CLOUD_PROJECT_ID no configurado en .env o settings.")
             return False
        if not region:
             logger.error("❌ GOOGLE_CLOUD_REGION no configurado en .env o settings.")
             return False

        # Inicializar aiplatform con project y location
        # Esto configura el cliente para usar las credenciales ADC y el proyecto/región
        aiplatform.init(project=project_id, location=region)

        # ────────────────────────────────────────────────────────────────────
        # ✅ Lógica de llamada a la API de Google Cloud Vertex AI (Modelo Imagen)
        # ────────────────────────────────────────────────────────────────────
        # Modelo de generación de imagen (ej. "imagegeneration@005" o "imagegeneration@002")
        # Asegúrate de que este modelo esté disponible y habilitado en tu proyecto/región.
        # Puedes encontrar los modelos disponibles en la consola de Vertex AI.
        model_name = "imagegeneration@005" # O la versión que desees usar (ej. "imagegeneration@002")

        # Crear el cliente de predicción
        # El endpoint se construye con el project_id, region y model_name
        endpoint = f"projects/{project_id}/locations/{region}/publishers/google/models/{model_name}"
        prediction_client = prediction_service.PredictionServiceClient()

        # Definir la instancia de entrada (el prompt)
        # Para imagegeneration@005, la instancia es un diccionario con la clave 'prompt'
        instances_list = [
            {"prompt": prompt_texto}
        ]

        # Definir los parámetros de generación (ej. número de imágenes, tamaño, etc.)
        # Los parámetros también son un diccionario
        parameters_dict = {
            "sampleCount": 1,
            "aspectRatio": "1:1", # "1:1", "16:9", "9:16", "4:3", "3:4"
            # "seed": 42, # Opcional
        }

        # Construir la PredictRequest
        # ✅ CORRECCIÓN: Pasar los diccionarios Python directamente
        # El SDK de aiplatform convierte automáticamente dicts a Value/Struct
        predict_request = PredictRequest(
            endpoint=endpoint,
            instances=instances_list, # ✅ Pasar la lista de diccionarios directamente
            parameters=parameters_dict, # ✅ Pasar el diccionario directamente
        )

        logger.info(f"🖼️ Enviando prompt a Google Cloud Vertex AI ({model_name}):\n{prompt_texto!r}")

        # Realizar la llamada de predicción
        response = prediction_client.predict(request=predict_request)

        # Procesar la respuesta
        if response.predictions:
            # Las imágenes generadas por el modelo Imagen suelen venir en base64
            # en el campo 'bytesBase64Encoded' dentro de la primera predicción.
            # La estructura exacta puede variar ligeramente según el modelo y la respuesta.
            image_data_base64 = response.predictions[0]["bytesBase64Encoded"]
            image_bytes = BytesIO(base64.b64decode(image_data_base64))

            # Guardar la imagen
            output_path_obj = Path(output_path)
            output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Asegurar que el directorio exista
            img = Image.open(image_bytes)
            img.save(output_path_obj)

            logger.info(f"✅ Imagen generada y guardada correctamente con Google Cloud Vertex AI en: {output_path}")
            print(f"\n🟢 IMAGEN GENERADA CON GOOGLE CLOUD VERTEX AI:")
            print(f"   Ruta: {output_path}")
            return True
        else:
            logger.error("❌ Google Cloud Vertex AI no devolvió predicciones de imagen.")
            return False

    except GoogleAPIError as e:
        # Captura errores específicos de la API de Google Cloud (ej. permisos, cuota, modelo no encontrado)
        logger.error(f"❌ Google Cloud API Error ({e.code}): {e.message}")
        print(f"\n🔴 ERROR DE GOOGLE CLOUD API ({e.code}):")
        print(f"   Detalle: {e.message}")
        return False
    except Exception as e:
        # Captura cualquier otra excepción inesperada
        error_type = type(e).__name__
        logger.error(f"❌ Error inesperado ({error_type}) al generar imagen con Google Cloud: {e}")
        print(f"\n🔴 ERROR INESPERADO ({error_type}):")
        print(f"   Detalle: {e}")
        return False


if __name__ == "__main__":
    # ──────────────────────────────────────────────────────────────────────────
    # Configura la autenticación de Google Cloud en tu entorno (WSL/Linux):
    # 1. Instala gcloud CLI (si no la tienes): https://cloud.google.com/sdk/docs/install
    # 2. Inicia sesión: gcloud auth login
    # 3. Configura credenciales por defecto: gcloud auth application-default login
    # 4. Establece el proyecto (opcional, pero recomendado): gcloud config set project your-project-id
    # ──────────────────────────────────────────────────────────────────────────

    # Asegúrate de tener GOOGLE_CLOUD_PROJECT_ID y GOOGLE_CLOUD_REGION en tu .env
    # También necesitas instalar: pip install google-cloud-aiplatform Pillow protobuf

    # ──────────────────────────────────────────────────────────────────────────
    # ✅ Prompt de prueba y ruta de salida
    # ──────────────────────────────────────────────────────────────────────────
    prompt_para_google = "A cute robot playing with a cat, digital art, children's book style" # Prompt de prueba para Google
    output_image_path = Path(settings.IMAGES_DIR) / "google_test_image.png"

    # Ejecutar la prueba de generación de imagen con Google Cloud
    test_google_image_generation(prompt_para_google, str(output_image_path))