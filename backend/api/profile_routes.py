# api/profile_routes.py
# Endpoints para crear y consultar perfiles infantiles

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.database import SessionLocal
from models.models import ChildProfile

# Crear Blueprint para los perfiles
profiles_bp = Blueprint('profiles', __name__)

# ──────────────────────────────────────────────────────
# POST /api/profiles
# Crear nuevo perfil infantil
# ──────────────────────────────────────────────────────
@profiles_bp.route('/api/profiles', methods=['POST'])
@jwt_required()
def crear_perfil():
    """
    Crea un nuevo perfil infantil asociado al adulto autenticado (JWT).
    """
    db = SessionLocal()
    try:
        data = request.get_json()

        nombre = data.get("nombre", "").strip()
        edad = data.get("edad")
        avatar_url = data.get("avatar_url") or None  # Puede venir vacío

        if not nombre or not edad:
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        adulto_email = get_jwt_identity()

        nuevo_perfil = ChildProfile(
            nombre=nombre,
            edad=edad,
            avatar_url=avatar_url,
            adulto_email=adulto_email
        )
        db.add(nuevo_perfil)
        db.commit()
        db.refresh(nuevo_perfil)

        return jsonify(nuevo_perfil.to_dict()), 201

    except Exception as e:
        return jsonify({"error": "Error al crear el perfil", "detail": str(e)}), 500
    finally:
        db.close()

# ──────────────────────────────────────────────────────
# GET /api/profiles
# Listar todos los perfiles infantiles del adulto
# ──────────────────────────────────────────────────────
@profiles_bp.route('/api/profiles', methods=['GET'])
@jwt_required()
def listar_perfiles():
    """
    Devuelve todos los perfiles infantiles del adulto autenticado (por JWT).
    """
    db = SessionLocal()
    try:
        adulto_email = get_jwt_identity()

        perfiles = db.query(ChildProfile).filter_by(adulto_email=adulto_email).all()
        perfiles_dict = [perfil.to_dict() for perfil in perfiles]

        return jsonify(perfiles_dict), 200

    except Exception as e:
        return jsonify({"error": "Error al listar los perfiles", "detail": str(e)}), 500
    finally:
        db.close()
