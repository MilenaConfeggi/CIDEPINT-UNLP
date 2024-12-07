from servicios.backend.src.core.config import Config
from flask import send_from_directory, jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioUsuario
from flask import session

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.get("/authenticate")
def authenticate():
    try:
        mail = request.args["mail"]
        password = request.args["password"]
        usuario = servicioUsuario.check_user(mail, password)
        session["mail"] = usuario.mail
        return jsonify({"info": "Sesión iniciada correctamente"}), 200
    except KeyError as e:
        return jsonify({"Error": "Parámetros faltantes o inválidos"}), 400
    except Exception as e:
        return jsonify({"Error": "El usuario y la contraseña no coinciden"}), 406

@bp.get("/logout")
def logout():
    if session.get("mail"):
        del session["mail"]
        session.clear()
        return jsonify({"info": "La sesión se cerró corectamente"}), 200
    else:
        return jsonify({"error": "No hay sesión activa"}), 406