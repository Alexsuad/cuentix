# backend/api/auth_routes.py
# Endpoints de autenticación y registro para adultos responsables (implementación real con DB y JWT)

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from config.database import SessionLocal
from models.models import User

# Crear el blueprint con prefijo global /api/auth
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# ───────────────────────────────────────────────────────────────
# POST /api/auth/register
# Registro real de un adulto, con verificación e inserción en DB
# ───────────────────────────────────────────────────────────────
@auth_bp.route('/register', methods=['POST'])
def register_adulto():
    data = request.get_json()
    nombre = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    birth_date = data.get("birth_date", "").strip()

    # Validaciones básicas
    if not nombre or not email or not password or not birth_date:
        return jsonify({"error": "Todos los campos son obligatorios."}), 400

    if len(password) < 6:
        return jsonify({"error": "La contraseña debe tener al menos 6 caracteres."}), 400

    db = SessionLocal()
    try:
        # Verifica si el correo ya está registrado
        if db.query(User).filter_by(correo=email).first():
            return jsonify({"error": "El email ya está registrado."}), 409

        # Hashea la contraseña antes de guardar
        hashed_password = pbkdf2_sha256.hash(password)
        nuevo_usuario = User(
            nombre=nombre,
            correo=email,
            contraseña=hashed_password,
            fecha_registro=datetime.utcnow()
        )
        db.add(nuevo_usuario)
        db.commit()

        return jsonify({"msg": "Usuario registrado exitosamente."}), 201

    except Exception as e:
        return jsonify({"error": "Error al registrar usuario.", "detail": str(e)}), 500

    finally:
        db.close()

# ───────────────────────────────────────────────────────────────
# POST /api/auth/login
# Verificación real de credenciales + JWT
# ───────────────────────────────────────────────────────────────
@auth_bp.route('/login', methods=['POST'])
def login_adulto():
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"error": "Email y contraseña obligatorios."}), 400

    db = SessionLocal()
    try:
        usuario = db.query(User).filter_by(correo=email).first()

        if not usuario or not pbkdf2_sha256.verify(password, usuario.contraseña):
            return jsonify({"error": "Credenciales inválidas."}), 401

        # Generar JWT válido por 3 horas
        token = create_access_token(
            identity=usuario.correo,
            expires_delta=timedelta(hours=3)
        )

        return jsonify({
            "access_token": token,
            "expires_in": 10800,
            "email": usuario.correo
        }), 200

    except Exception as e:
        return jsonify({"error": "Error en el inicio de sesión.", "detail": str(e)}), 500

    finally:
        db.close()
