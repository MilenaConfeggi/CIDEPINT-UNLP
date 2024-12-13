from models import db
from models.usuarios.permiso import Permiso
from models.usuarios.rol import Rol
from models.usuarios.rol_permiso import RolPermiso
from models.usuarios.usuario import Usuario
from models.personal.empleado import Empleado
from datetime import datetime
from web import bcrypt
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

def crear_usuario(data):
    if Usuario.query.filter_by(mail=data.get('mail'), esta_borrado=False).first() is not None:
        raise ValueError("Ya existe un usuario con ese mail")


    if data.get('rol').nombre == "jefe_de_area":
        jefesDeAreas = Usuario.query.filter_by(rol=data.get('rol'), esta_borrado=False).all()
        empleadosJefesDeArea = ()
        for jefe in jefesDeAreas:
            emp = Empleado.query.filter_by(usuario_servicio_id=jefe.id).first()
            if emp is not None and emp.area == data.get('empleado').area:
                raise ValueError("Ya existe un jefe de area para esa área, por favor saque al jefe de área anterior para ingresar uno nuevo")

    cambiar = True
    if data.get('cambiar_contra') is not None:
        cambiar = data.get('cambiar_contra')

    nuevo_usuario = Usuario(
        mail=data.get('mail'),
        contra=bcrypt.generate_password_hash(data.get('contra').encode("utf-8")),
        rol=data.get('rol'),
        cambiar_contra=cambiar,
    )
    db.session.add(nuevo_usuario)
    data.get('empleado').usuario_servicio = nuevo_usuario
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
    empleado = Empleado.query.filter_by(usuario_servicio=usuario).first()
    empleado.usuario_servicio = None
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

@jwt_required()
def tiene_permiso(permiso):
    user_mail = get_jwt_identity()
    usuario = obtener_usuario_por_mail(user_mail)
    if usuario.system_admin == True:
        return True
    if usuario.cambiar_contra:
        return False
    permissions = obtener_permisos(usuario)

    return usuario is not None and permiso in permissions

def buscar_rol_por_id(rol_id):
    return Rol.query.filter_by(id=rol_id).first()

def listar_roles():
    return Rol.query.all()

def listar_empleados():
    return Empleado.query.filter_by(usuario_servicio=None).all()

@jwt_required()
def cambiar_contra(password):
    user_mail = get_jwt_identity()
    usuario = obtener_usuario_por_mail(user_mail)
    usuario.contra = bcrypt.generate_password_hash(password.encode("utf-8"))
    usuario.cambiar_contra = False
    db.session.commit()
    return True
