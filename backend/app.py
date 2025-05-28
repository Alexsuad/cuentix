# backend/app.py
# Punto de entrada principal del backend Cuentix

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

from config.database import engine
from models.models import Base
from api.story_routes import stories_bp
from api.auth_routes import auth_bp
from api.profile_routes import profiles_bp

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

# Servir páginas HTML desde /frontend/pages/
@app.route('/pages/<path:filename>')
def serve_pages(filename):
    pages_dir = os.path.join(os.path.dirname(__file__), '../frontend/pages')
    return send_from_directory(pages_dir, filename)

# Servir assets como CSS, JS, imágenes desde /frontend/assets/
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    assets_dir = os.path.join(os.path.dirname(__file__), '../frontend/assets')
    return send_from_directory(assets_dir, filename)