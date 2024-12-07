from datetime import datetime
from servicios.backend.src.core.services.servicioUsuario import crear_usuario, crear_rol
from models.usuarios.rol import Rol
from models.base import db
from web import bcrypt

"""

def seeds_usuarios():
    seed_usuarios()

def seed_usuarios():
    rol_trabajador = crear_rol({'nombre':"trabajador"})
    db.session.add(rol_trabajador)
    rol_jefe_de_area = crear_rol({'nombre':"jefe_de_area"})
    db.session.add(rol_jefe_de_area)
    rol_administrador = crear_rol({'nombre':"administrador"})
    db.session.add(rol_administrador)
    db.session.commit()

    usuario1 = crear_usuario({
        'mail':"pepito@example.com",'contra':bcrypt.generate_password_hash("123".encode("utf-8")),'rol':rol_trabajador
    })
    usuario2 = crear_usuario({
        'mail':"moniquita@example.com",'contra':bcrypt.generate_password_hash("321".encode("utf-8")),'rol':rol_jefe_de_area
    })
    usuario3 = crear_usuario({
        'mail':"admin@example.com",'contra':bcrypt.generate_password_hash("soyadmin".encode("utf-8")),'rol':rol_administrador
    })
    db.session.add(usuario1)
    db.session.add(usuario2)
    db.session.add(usuario3)
    db.session.commit()

"""
