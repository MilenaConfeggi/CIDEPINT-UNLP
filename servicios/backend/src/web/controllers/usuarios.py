from servicios.backend.src.core.config import Config
from werkzeug.utils import secure_filename, safe_join
from flask import send_from_directory, jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioUsuario
from servicios.backend.src.web.schemas.usuarios import usuariosSchema
from flask import session
from flask import jsonify

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.get("/")
def listar_usuarios():
    usuarios = servicioUsuario.listar_usuarios()
    data = usuariosSchema.dump(usuarios, many=True)
    return jsonify(data), 200

@bp.get("/authenticate/")
def authenticate():
    try:
        mail = request.args["mail"]
        password = request.args["password"]
        usuario = servicioUsuario.check_user(mail, password)
        session["mail"] = usuario.mail
        return jsonify({"logueo": "exitoso"}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 400

