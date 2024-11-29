from datetime import datetime
from servicios.backend.src.core.services.servicioUsuario import crear_usuario, crear_rol
from models.usuarios.rol import Rol
from models.base import db

def seeds_usuarios():
    seed_usuarios()

def seed_usuarios():
    rol_trabajador = crear_rol({'nombre':"trabajador"})
    db.session.add(rol_trabajador)
    db.session.commit()

    usuario1 = crear_usuario({
        'mail':"pepito@example.com",'contra':123,'rol':rol_trabajador
    })
    db.session.add(usuario1)
    db.session.commit()
