# backend\app.py
# Punto de entrada para la API REST de Cuentix (Wizard, generación, descarga)

from flask import Flask
from flask_cors import CORS

# Importar rutas de la API
from api.story_routes import stories_bp

# Crear la app Flask
app = Flask(__name__)

# Habilitar CORS para permitir llamadas desde el frontend
CORS(app)

# Registrar las rutas agrupadas en blueprints
app.register_blueprint(stories_bp)
