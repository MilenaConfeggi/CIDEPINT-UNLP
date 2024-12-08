from flask import session
from servicios.backend.src.core.services import servicioUsuario

def is_authenticated():
    return session.get("mail") is not None

def check_permission(permission):
    return servicioUsuario.tiene_permiso(permiso)