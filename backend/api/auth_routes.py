# api/auth_routes.py
# Endpoint temporal para simular autenticación de adultos y emitir JWT

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/login', methods=['POST'])
def login_adulto():
    """
    Endpoint temporal que simula login de un adulto.
    Recibe un email y devuelve un token JWT.
    """
    data = request.get_json()
    email = data.get("email", "").strip()

    if not email:
        return jsonify({"error": "Email requerido"}), 400

    # Simulación: aceptar cualquier email como válido
    access_token = create_access_token(
        identity=email,
        expires_delta=datetime.timedelta(hours=3)
    )

    return jsonify({
        "access_token": access_token,
        "expires_in": 10800,  # 3 horas en segundos
        "email": email
    }), 200
