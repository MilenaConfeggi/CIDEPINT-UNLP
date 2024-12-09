from servicios.backend.src.core.config import Config
from flask import send_from_directory, jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioUsuario
from flask_jwt_extended import jwt_required, create_access_token
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.post("/authenticate")
def authenticate():
    try:
        mail = request.json.get("mail")
        password = request.json.get("password")
        print(mail, password)
        usuario = servicioUsuario.check_user(mail, password)
        access_token = create_access_token({"mail": mail, "password":password}, Config.JWT_SECRET)
        return jsonify({"info": "Sesión iniciada correctamente", "access_token":access_token}), 200
    except KeyError as e:
        return jsonify({"Error": "Parámetros faltantes o inválidos"}), 400
    except Exception as e:
        print(e)
        return jsonify({"Error": "El usuario y la contraseña no coinciden"}), 406
