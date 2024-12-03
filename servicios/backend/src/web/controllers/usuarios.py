from servicios.backend.src.core.config import Config
from flask import jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioUsuario
from servicios.backend.src.web.schemas.usuarios import usuariosSchema

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.get("/")
def listar_usuarios():
    usuarios = servicioUsuario.listar_usuarios()
    data = usuariosSchema.dump(usuarios, many=True)
    return jsonify(data), 200


