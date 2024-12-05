from servicios.backend.src.core.services import servicioUsuario
from flask_jwt_extended import jwt_required

@jwt_required()
def check_permission(permiso):
    return servicioUsuario.tiene_permiso(permiso)