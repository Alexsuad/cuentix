# api/story_routes.py
# Rutas API para gestión de historias (crear, consultar estado, descargar video).
# Funciona con almacenamiento temporal en memoria (STORIES_DB) para MVP.

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, send_file
from models.models import Story, ChildProfile
from config.database import SessionLocal
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
@jwt_required()
def start_story():
    """
    Crea una nueva historia asociada a un perfil infantil del adulto autenticado.
    """
    db = SessionLocal()

    try:
        data = request.get_json()

        # Validación mínima de campos
        required_fields = [
            "nombre", "edad", "personaje_principal",
            "lugar", "objeto_magico", "villano", "tipo_final", "profile_id"
        ]

        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        profile_id = data["profile_id"]
        adulto_email = get_jwt_identity()

        # Verificar que el perfil exista y sea del adulto autenticado
        perfil = db.query(ChildProfile).filter_by(id=profile_id, adulto_email=adulto_email).first()

        if not perfil:
            return jsonify({"error": "Perfil inválido o no pertenece a este usuario"}), 403

        # Crear historia
        story_id = str(uuid.uuid4())

        nueva_historia = Story(
            id=story_id,
            profile_id=profile_id,
            status="pending"
        )

        db.add(nueva_historia)
        db.commit()

        # Lanzar generación (mantendremos STORIES_DB temporalmente para el MVP)
        from utils.db_memory import STORIES_DB
        STORIES_DB[story_id] = nueva_historia

        from core.orchestrator import start_story_generation
        start_story_generation(story_id, data)

        return jsonify({"story_id": story_id}), 201

    except Exception as e:
        return jsonify({"error": "Error al crear la historia", "detail": str(e)}), 500

    finally:
        db.close()


# ──────────────────────────────────────────────────────────────
# GET /api/stories/<story_id>/status
# Consulta el estado actual de una historia
# ──────────────────────────────────────────────────────────────
@stories_bp.route('/api/stories/<story_id>/status', methods=['GET'])
@jwt_required()
def get_story_status(story_id):
    """
    Consulta el estado actual de una historia, incluyendo el perfil asociado.
    """
    from config.database import SessionLocal
    db = SessionLocal()

    try:
        story = db.query(Story).filter_by(id=story_id).first()

        if not story:
            return jsonify({"error": "Historia no encontrada."}), 404

        response = {
            "story_id": story.id,
            "status": story.status,
            "profile_id": story.profile_id
        }

        if story.status == "completed" and story.video_path:
            response["video_url"] = story.video_path

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Error al consultar la historia", "detail": str(e)}), 500

    finally:
        db.close()



# ──────────────────────────────────────────────────────────────
# GET /api/stories/<story_id>/download
# Permite visualizar o descargar el video generado
# ──────────────────────────────────────────────────────────────
@stories_bp.route('/api/stories/<story_id>/download', methods=['GET'])
@jwt_required()
def download_story_video(story_id):

    """
    Permite visualizar o descargar el video generado de una historia.
    """
    from config.database import SessionLocal
    db = SessionLocal()

    try:
        # Buscar la historia en la base de datos
        story = db.query(Story).filter_by(id=story_id).first()

        if not story:
            return jsonify({"error": "Historia no encontrada."}), 404

        if story.status != "completed" or not story.video_path:
            return jsonify({"error": "El video aún no está disponible."}), 400

        if not os.path.isfile(story.video_path):
            return jsonify({"error": "El archivo de video no existe."}), 500

        # Enviar el archivo de video desde su ruta real
        return send_file(story.video_path, as_attachment=False)

    except Exception as e:
        return jsonify({"error": "Error interno al descargar el video.", "detail": str(e)}), 500

    finally:
        db.close()
