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
    if Usuario.query.filter_by(mail=data.get('mail'), esta_borrado=False).first():
        raise ValueError("Ya existe un usuario con ese mail")
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

def crear_permiso(data):
    nuevo_permiso = Permiso(
        nombre=data.get('nombre'),
    )
    db.session.add(nuevo_permiso)
    db.session.commit()
    return nuevo_permiso

def asignar_permiso(data):
    rol_permiso = RolPermiso(rol=data.get('rol'), permiso=data.get('permiso'))
    db.session.add(rol_permiso)
    db.session.commit()

def listar_usuarios():
    usuarios = Usuario.query.filter_by(esta_borrado=False).all()
    return usuarios

def eliminar_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if usuario is None:
        raise ValueError("No se encontró el usuario seleccionado")
    usuario.esta_borrado = True
    db.session.commit()

def obtener_usuario_por_mail(email):
    usuario = Usuario.query.filter_by(mail=email, esta_borrado=False).first()
    return usuario

def check_user(usermail, password):
    """
    Si el usuario existe y las contraseñas coinciden devuelve el usuario, sino devuelve None
    """
    usuario = obtener_usuario_por_mail(usermail)
    print(usuario)
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


def tiene_permiso(permiso):
    user_mail = session.get("user")
    usuario = obtener_usuario_por_mail(user_mail)
    if usuario.system_admin == True:
        return True
    permissions = obtener_permisos(usuario)

    return usuario is not None and permission in permissions