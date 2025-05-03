# app.py
# Punto de entrada principal del backend Cuentix

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.database import engine
from models.models import Base
from api.story_routes import stories_bp
from api.auth_routes import auth_bp
from api.profile_routes import profiles_bp



app = Flask(__name__)
CORS(app)

# Configurar clave secreta para JWT (⚠ cambiar por una segura en producción)
app.config['JWT_SECRET_KEY'] = 'clave-secreta-super-cuentix'
jwt = JWTManager(app)

# Crear tablas (si no existen)
Base.metadata.create_all(bind=engine)

# Registrar Blueprints
app.register_blueprint(stories_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profiles_bp)

# Mensaje de prueba
@app.route("/")
def index():
    return {"msg": "Cuentix Backend funcionando"}
