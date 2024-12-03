from models import db
from models.usuarios.permiso import Permiso
from models.usuarios.rol import Rol
from models.usuarios.rol_permiso import RolPermiso
from models.usuarios.usuario import Usuario
from datetime import datetime
from web import bcrypt
from flask import session
from flask import request

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

def obtener_usuario_por_mail(email):
    usuario = Usuario.query.filter_by(mail=email).first()
    return usuario

def check_user(usermail, password):
    """
    Si el usuario existe y las contraseñas coinciden devuelve el usuario, sino devuelve None
    """
    usuario = obtener_usuario_por_mail(usermail)
    if (not usuario) or (
        not (
            usuario.contra and bcrypt.check_password_hash(usuario.contra, password)
        )
    ):
        raise ValueError("Usuario y/o contraseña incorrecta")
    return usuario

def obtener_permisos(user):
    user_rol = user.rol.nombre
    a = (
        db.session.query(Permiso.nombre)
        .join(RolPermiso)
        .join(Rol)
        .filter(Rol.nombre == user_rol)
        .all()
    )
    flat_permisos = tuple(item for sublist in a for item in sublist)
    return flat_permisos


def tiene_permiso(session, permiso):
    user_mail = session.get("user")
    usuario = obtener_usuario_por_mail(user_mail)
    if usuario.system_admin == True:
        return True
    permissions = obtener_permisos(usuario)

    return usuario is not None and permission in permissions