# api/story_routes.py
# Rutas API para gestión de historias (crear, consultar estado, descargar video).
# Funciona con almacenamiento temporal en memoria (STORIES_DB) para MVP.

from flask import Blueprint, request, jsonify, send_file
from models.models import Story
from core.orchestrator import start_story_generation
from utils.db_memory import STORIES_DB  # ✅ Fuente única para almacenamiento en memoria
import uuid
import os

# Crear Blueprint para agrupar rutas relacionadas con historias
stories_bp = Blueprint('stories', __name__)

# Campos mínimos requeridos por el wizard para crear una historia
REQUIRED_FIELDS = [
    "nombre", "edad", "personaje_principal", "lugar",
    "objeto_magico", "villano", "tipo_final"
]

# Estados válidos posibles (puede usarse para validación futura)
VALID_STATUSES = ["pending", "generating", "completed", "failed"]

# ──────────────────────────────────────────────────────────────
# POST /api/stories/start
# Crea una nueva historia y lanza el proceso de generación
# ──────────────────────────────────────────────────────────────
@stories_bp.route('/api/stories/start', methods=['POST'])
def start_story():
    """
    Recibe las elecciones del wizard, crea una nueva historia y lanza el proceso de generación.
    """
    try:
        # 1. Obtener datos del JSON enviado
        data = request.get_json()

        # 2. Validar campos requeridos
        if not all(field in data for field in REQUIRED_FIELDS):
            return jsonify({"error": "Datos incompletos en la solicitud."}), 400

        # 3. Generar ID único para la historia
        story_id = str(uuid.uuid4())

        # 4. Crear instancia de Story (estado inicial: pending)
        new_story = Story(
            id=story_id,
            profile_id=data.get("profile_id", "default"),  # Campo opcional para MVP
            status="pending"
        )

        # 5. Guardar historia en memoria
        STORIES_DB[story_id] = new_story

        # 6. Iniciar proceso de generación (hilo separado)
        start_story_generation(story_id, data)

        # 7. Responder al frontend con el ID generado
        return jsonify({"story_id": story_id}), 201

    except Exception as e:
        return jsonify({"error": "Error interno al iniciar la historia.", "detail": str(e)}), 500


# ──────────────────────────────────────────────────────────────
# GET /api/stories/<story_id>/status
# Consulta el estado actual de una historia
# ──────────────────────────────────────────────────────────────
@stories_bp.route('/api/stories/<story_id>/status', methods=['GET'])
def get_story_status(story_id):
    """
    Consulta el estado actual de una historia (pending, generating, completed, failed).
    """
    try:
        # 1. Buscar la historia en memoria
        story = STORIES_DB.get(story_id)

        if not story:
            return jsonify({"error": "Historia no encontrada."}), 404

        # 2. Preparar respuesta según el estado
        response = {
            "story_id": story.id,
            "status": story.status
        }

        # 3. Si está terminada, incluir URL del video
        if story.status == "completed" and story.video_path:
            response["video_url"] = story.video_path

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Error interno al consultar la historia.", "detail": str(e)}), 500


# ──────────────────────────────────────────────────────────────
# GET /api/stories/<story_id>/download
# Permite visualizar o descargar el video generado
# ──────────────────────────────────────────────────────────────
@stories_bp.route('/api/stories/<story_id>/download', methods=['GET'])
def download_story_video(story_id):
    """
    Permite visualizar o descargar el video generado de una historia.
    """
    try:
        # 1. Buscar la historia en memoria
        story = STORIES_DB.get(story_id)

        if not story:
            return jsonify({"error": "Historia no encontrada."}), 404

        if story.status != "completed" or not story.video_path:
            return jsonify({"error": "El video aún no está disponible."}), 400

        # 2. Extraer ruta y nombre del archivo
        return send_file(story.video_path, as_attachment=False)

    except Exception as e:
        return jsonify({"error": "Error interno al descargar el video.", "detail": str(e)}), 500
