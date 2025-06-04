# ────────────────────────────────────────────────────────────────────────────
# File: backend/app.py
# Punto de entrada principal del backend Cuentix
# ────────────────────────────────────────────────────────────────────────────

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
import uuid

from config.database import engine
from models.models import Base
from api.story_routes import stories_bp
from api.auth_routes import auth_bp
from api.profile_routes import profiles_bp
from core.orchestrator import start_story_generation
from config.database import SessionLocal
from models.models import Story

# ─────────────────────────────────────────────
# 🚀 Configuración base de la aplicación Flask
# ─────────────────────────────────────────────

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5501"}}, supports_credentials=True)

# Clave secreta para JWT (⚠️ cambia en producción)
app.config['JWT_SECRET_KEY'] = 'clave-secreta-super-cuentix'
jwt = JWTManager(app)

# Crear tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# Registrar rutas del sistema (blueprints)
app.register_blueprint(stories_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profiles_bp)

# Ruta principal de prueba
@app.route("/")
def index():
    return {"msg": "Cuentix Backend funcionando"}

# ─────────────────────────────────────────────
# 🌐 Servir archivos estáticos del frontend
# ─────────────────────────────────────────────

@app.route('/pages/<path:filename>')
def serve_pages(filename):
    pages_dir = os.path.join(os.path.dirname(__file__), '../frontend/pages')
    return send_from_directory(pages_dir, filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    assets_dir = os.path.join(os.path.dirname(__file__), '../frontend/assets')
    return send_from_directory(assets_dir, filename)

# ─────────────────────────────────────────────
# 🎞️ Servir archivos generados dinámicamente
# ─────────────────────────────────────────────

@app.route('/videos/<path:filename>')
def serve_videos(filename):
    videos_dir = os.path.join(os.path.dirname(__file__), 'output')
    return send_from_directory(videos_dir, filename)

@app.route('/text/<path:filename>')
def serve_text_files(filename):
    text_dir = os.path.join(os.path.dirname(__file__), 'assets', 'text')
    return send_from_directory(text_dir, filename)

# ─────────────────────────────────────────────
# 🧠 Endpoint para iniciar la generación del cuento
# ─────────────────────────────────────────────

@app.route("/api/stories/start", methods=["POST"])
def iniciar_generacion():
    try:
        datos = request.get_json()
        story_id = str(uuid.uuid4())

        # ⚠️ Corrección: orden correcto de argumentos (story_id, datos)
        start_story_generation(story_id, datos)

        return jsonify({
            "story_id": story_id,
            "status": "pendiente"  # Ya no bloquea, correcto para asincronía
        }), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────────
# 📊 Endpoint para consultar el estado de generación
# ─────────────────────────────────────────────

@app.route("/api/stories/<story_id>/status", methods=["GET"])
def consultar_estado(story_id):
    db = SessionLocal()
    try:
        historia = db.query(Story).filter_by(id=story_id).first()

        if not historia:
            return jsonify({"error": "Historia no encontrada"}), 404

        respuesta = {
            "story_id": historia.id,
            "status": historia.status,
            "video_url": historia.video_path,
            "thumbnail_url": historia.thumbnail_url,
            "text_url": historia.story_text_url,
            "subtitles_url": historia.subtitles_url,
            "error_message": historia.error_message
        }

        return jsonify(respuesta), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()