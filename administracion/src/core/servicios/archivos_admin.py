
import os
from werkzeug.utils import secure_filename
from flask import current_app
from sqlalchemy import extract
from models.base import db
from models.archivos_admin.archivo import Archivo
from models.archivos_admin.carpeta import Carpeta, usuarios_leen_carpeta
from flask_login import current_user
from datetime import datetime
from sqlalchemy.sql import expression

def listar_archivos_de_carpeta(id_carpeta):
    query = Archivo.query.filter(Archivo.id_carpeta == id_carpeta)
    
    return query.order_by(Archivo.nombre.asc()).all()


def listar_carpetas(anio):
    if current_user.rol != 'Personal':
        return Carpeta.query.filter(
            (extract('year', Carpeta.fecha_ingreso) == anio) | (Carpeta.id_fondo.isnot(None))
        ).order_by(Carpeta.nombre.asc()).all()
    else:
        return Carpeta.query.join(usuarios_leen_carpeta).filter(
            (extract('year', Carpeta.fecha_ingreso) == anio) & 
            ((usuarios_leen_carpeta.c.id_user == current_user.id) | (Carpeta.id_fondo.isnot(None)))
        ).order_by(Carpeta.nombre.asc()).all()


def crear_carpeta(
    nombre,
    usuarios_leen,
    usuarios_editan,
    fondo
):
    nueva_carpeta = Carpeta(
            nombre=nombre,
            usuarios_editan=usuarios_editan,
            usuarios_leen=usuarios_leen,
            id_fondo=fondo
            )
    
    db.session.add(nueva_carpeta)
    db.session.commit()
    
    return nueva_carpeta


def conseguir_carpeta_de_id(id_carpeta):
    return Carpeta.query.get(id_carpeta)

def conseguir_archivo_de_id(id_archivo):
    return Archivo.query.get(id_archivo)

def generar_nombre_unico(directorio, nombre):
    base, extension = os.path.splitext(nombre)  # Divide el nombre y la extensión
    contador = 1
    nuevo_nombre = nombre
    while os.path.exists(os.path.join(directorio, nuevo_nombre)):
        nuevo_nombre = f"{base}_{contador}{extension}"  # Agrega un sufijo numérico
        contador += 1
    return nuevo_nombre


def conseguir_directorio(id_carpeta):
    carpeta = conseguir_carpeta_de_id(id_carpeta)
    return os.path.join(current_app.root_path,'archivos',carpeta.nombre)



def guardar_archivo_en_carpeta(id_carpeta, archivo):

    nombre = secure_filename(archivo.filename)
    directorio = conseguir_directorio(id_carpeta)

    if not os.path.exists(directorio):
        os.makedirs(directorio)

    nombre = generar_nombre_unico(directorio, nombre)
    filepath = os.path.join(directorio, nombre)
    archivo.save(filepath)

    carpeta = conseguir_carpeta_de_id(id_carpeta)
    # Guardar en la base de datos
    nuevo_archivo = Archivo(nombre=nombre, carpeta=carpeta, filepath=filepath)

    db.session.add(nuevo_archivo)
    db.session.commit()
    return nuevo_archivo


def eliminar_archivo(id_archivo):

    archivo = Archivo.query.get(id_archivo)
    if archivo:
        os.remove(archivo.filepath)
        db.session.delete(archivo)
        db.session.commit()
        return True
    return False


def eliminar_carpeta(id_carpeta):
    
    carpeta = Carpeta.query.get(id_carpeta)
    if carpeta:
        for archivo in carpeta.archivos:
            eliminar_archivo(archivo.id)
        directorio = conseguir_directorio(id_carpeta)
        if os.path.exists(directorio) and os.path.isdir(directorio):
            os.rmdir(directorio)
        db.session.delete(carpeta)
        db.session.commit()
        return True
    return False


def chequear_nombre_carpeta_existente(nombre):
    carpeta = Carpeta.query.filter(
        Carpeta.nombre == nombre,
        extract('year', Carpeta.fecha_ingreso) == datetime.now().year
    ).first()
    if carpeta:
        return True
    return False


def editar_carpeta(
    id_carpeta,
    nombre,
    usuarios_leen,
    usuarios_editan,
):
    
    carpeta = conseguir_carpeta_de_id(id_carpeta)
    
    carpeta.nombre = nombre
    carpeta.usuarios_leen = usuarios_leen
    carpeta.usuarios_editan = usuarios_editan

    db.session.commit()
    
    return carpeta
def get_carpeta_by_nombre(nombre):
    return Carpeta.query.filter(Carpeta.nombre == nombre).first()