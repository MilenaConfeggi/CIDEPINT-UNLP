from servicios.backend.src.core.config import Config
from flask import jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioUsuario
from servicios.backend.src.web.schemas.usuarios import usuariosSchema
from servicios.backend.src.web.helpers.auth import is_authenticated, check_permission

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.get("/")
def listar_usuarios():
    usuarios = servicioUsuario.listar_usuarios()
    data = usuariosSchema.dump(usuarios, many=True)
    return jsonify(data), 200

@bp.get("/delete")
def borrar_usuario():
    try:
        servicioUsuario.eliminar_usuario(id_usuario)
        return jsonify({"info": "Usuario borrado exitosamente"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 406



