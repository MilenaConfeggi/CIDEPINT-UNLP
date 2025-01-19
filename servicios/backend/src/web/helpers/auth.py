from flask import session
from servicios.backend.src.core.services import servicioUsuario
from flask_jwt_extended import get_jwt_identity, jwt_required

@jwt_required()
def is_authenticated():
    return get_jwt_identity() is not None

def check_permission(permission):
    return servicioUsuario.tiene_permiso(permission)