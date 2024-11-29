from servicios.backend.src.core.config import Config
from werkzeug.utils import secure_filename, safe_join
from flask import send_from_directory, jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioUsuario
from servicios.backend.src.web.schemas.usuarios import usuariosSchema

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.get("/")
def listar_usuarios():
    usuarios = servicioUsuario.listar_usuarios()
    data = usuariosSchema.dump(usuarios, many=True)
    return jsonify(data), 200
