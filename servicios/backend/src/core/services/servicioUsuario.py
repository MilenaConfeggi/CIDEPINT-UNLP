from models import db
from models.usuarios.permiso import Permiso
from models.usuarios.rol import Rol
from models.usuarios.rol_permiso import RolPermiso
from models.usuarios.usuario import Usuario
from datetime import datetime

def crear_usuario(data):
    nuevo_usuario = Usuario(
        mail=data.get('mail'),
        contra=data.get('contra'),
        rol=data.get('rol'),
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario

def crear_rol(data):
    nuevo_rol = Rol(
        nombre=data.get('nombre'),
    )
    db.session.add(nuevo_rol)
    db.session.commit()
    return nuevo_rol

def listar_usuarios():
    usuarios = Usuario.query.all()
    return usuarios

def eliminar_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    db.session.delete(usuario)
    db.session.commit()