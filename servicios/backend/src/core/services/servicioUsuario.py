from models import db
from models.usuarios.permiso import Permiso
from models.personal.area import Area
from models.usuarios.rol import Rol
from models.usuarios.rol_permiso import RolPermiso
from models.usuarios.usuario import Usuario
from models.personal.empleado import Empleado
from datetime import datetime
from web import bcrypt
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from servicios.backend.src.core.config import config

def generar_contrasena_aleatoria(longitud=14):
    caracteres = string.ascii_letters + string.digits
    contrasena = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return contrasena

def enviar_contrasena_por_mail(mail, contrasena):
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(config["development"].MAIL_USER, config["development"].MAIL_PASSWORD)

    msg = MIMEMultipart()
    msg["From"] = config["development"].MAIL_USER
    correo = mail
    msg["To"] = correo
    msg["Subject"] = "Contraseña usuario CIDEPINT (Area de Servicios)"

    body = "Esta es su contraseña provisional para iniciar sesión en el sistema de CIDEPINT, luego deberá cambiarla: "
    body = body + contrasena
    msg.attach(MIMEText(body, 'plain'))

    servidor.sendmail(config["development"].MAIL_USER, correo, msg.as_string())
    servidor.quit()

def crear_usuario(data):
    empleado = Empleado.query.filter_by(email=data.get('mail')).first()
    if empleado is None:
        raise ValueError("No existe un empleado con ese mail, por favor primero agregue un empleado con el mismo mail")

    if Usuario.query.filter_by(mail=data.get('mail'), esta_borrado=False).first() is not None:
        raise ValueError("Ya existe un usuario con ese mail")

    #verifico que no pueda haber usuarios jefes de areas en la misma área
    if data.get('rol').nombre == "Jefe de area":
        jefesDeAreas = Usuario.query.filter_by(rol=data.get('rol'), esta_borrado=False).all()
        for jefe in jefesDeAreas:
            emp = Empleado.query.filter_by(usuario_servicio_id=jefe.id).first()
            if emp is not None and emp.area == empleado.area:
                raise ValueError("Ya existe un jefe de area para esa área, por favor saque al jefe de área anterior para ingresar uno nuevo")

    usuario = Usuario.query.filter_by(mail=data.get('mail'), esta_borrado=True).first()
    if usuario is not None:
        contrasena = generar_contrasena_aleatoria()
        usuario.contra=bcrypt.generate_password_hash(contrasena.encode("utf-8"))
        usuario.rol=data.get('rol')
        usuario.esta_borrado=False
        usuario.cambiar_contra=True
        db.session.commit()
        return usuario
    

    cambiar = True
    if data.get('cambiar_contra') is not None:
        cambiar = data.get('cambiar_contra')

    if data.get('contra')is not None:
        nuevo_usuario = Usuario(
            mail=data.get('mail'),
            contra=bcrypt.generate_password_hash(data.get('contra').encode("utf-8")),
            rol=data.get('rol'),
            cambiar_contra=cambiar,
        )
        db.session.add(nuevo_usuario)
        empleado.usuario_servicio = nuevo_usuario
        db.session.commit()
        return nuevo_usuario
    else:
        contrasena = generar_contrasena_aleatoria()
        nuevo_usuario = Usuario(
            mail=data.get('mail'),
            contra=bcrypt.generate_password_hash(contrasena.encode("utf-8")),
            rol=data.get('rol'),
            cambiar_contra=cambiar,
        )
        db.session.add(nuevo_usuario)
        empleado.usuario_servicio = nuevo_usuario
        enviar_contrasena_por_mail(data.get('mail'), contrasena)
        db.session.commit()
        return nuevo_usuario

def recuperar_contra(data):
    mail = data.get('mail')
    usuario = obtener_usuario_por_mail(mail)

    contrasena = generar_contrasena_aleatoria()

    usuario.contra = bcrypt.generate_password_hash(contrasena.encode("utf-8"))
    usuario.cambiar_contra = True

    enviar_contrasena_por_mail(mail, contrasena)

    db.session.commit()
    return usuario

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

def listar_areas():
    areas = Area.query.all()
    return areas

def listar_usuarios_por_area(area_id):
    usuarios = (
        Usuario.query
        .join(Empleado, Empleado.usuario_servicio_id == Usuario.id)  # Unir las tablas Usuario y Empleado
        .filter(
            Empleado.area_id == area_id,  # Filtrar por el área específica
            Usuario.esta_borrado == False  # Asegurarse de que el usuario no está borrado
        )
        .all()
    )
    return usuarios

def cambiar_jefe_area(data):
    ja = buscar_rol_por_id(2)
    esclavo = buscar_rol_por_id(1)
    jefeAnterior = (
        Usuario.query
        .join(Empleado, Empleado.usuario_servicio_id == Usuario.id)  # Unir las tablas Usuario y Empleado
        .filter(
            Empleado.area_id == data.get('area_id'),  # Filtrar por el área específica
            Usuario.esta_borrado == False,  # Asegurarse de que el usuario no está borrado
            Usuario.rol_id == ja.id
        )
        .first()
    )
    jefeNuevo = Usuario.query.filter_by(id=data.get('usuario_id')).first()
    jefeAnterior.rol = esclavo
    jefeNuevo.rol = ja
    db.session.commit()

def eliminar_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if usuario is None:
        raise ValueError("No se encontró el usuario seleccionado")
    usuario.esta_borrado = True
    db.session.commit()

def obtener_usuario_por_mail(email):
    usuario = Usuario.query.filter_by(mail=email, esta_borrado=False).first()
    return usuario

def obtener_empleado_por_mail(email):
    empleado = Empleado.query.filter_by(email=email).first()  
    return empleado

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


def es_jefe_de_area(usuario):
    return usuario.rol.nombre == "Jefe de area"

def es_director(usuario):  
    return usuario.rol.nombre == "Director"

def es_secretaria(usuario):
    return usuario.rol.nombre == "Secretaria"

def listar_usuarios_paginados(page, per_page):
    return Usuario.query.filter_by(esta_borrado=False).paginate(page=page, per_page=per_page)
