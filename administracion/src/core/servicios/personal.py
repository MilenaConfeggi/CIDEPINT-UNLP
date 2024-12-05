import os
from werkzeug.utils import secure_filename
from flask import current_app
from sqlalchemy import extract
from models.base import db
from models.personal.empleado import Empleado
from models.archivos_admin.archivo import Archivo
from administracion.src.core.servicios import archivos_admin as servicio_archivos

def conseguir_empleado_de_id(id_empleado):
    return Empleado.query.get(id_empleado)


def conseguir_directorio(id_empleado):
    empleado = conseguir_empleado_de_id(id_empleado)
    return os.path.join(current_app.root_path,'archivos',empleado.user.username)



def guardar_archivo(id_empleado, archivo, tipo):

    nombre = secure_filename(archivo.filename)
    directorio = conseguir_directorio(id_empleado)

    if not os.path.exists(directorio):
        os.makedirs(directorio)

    nombre = servicio_archivos.generar_nombre_unico(directorio, nombre)
    filepath = os.path.join(directorio, nombre)
    archivo.save(filepath)

    empleado = conseguir_empleado_de_id(id_empleado)
    # Guardar en la base de datos
    nuevo_archivo = Archivo(nombre=nombre, empleado=empleado, filepath=filepath, tipo=tipo)

    db.session.add(nuevo_archivo)
    db.session.commit()


def eliminar_archivo(id_archivo):

    archivo = Archivo.query.get(id_archivo)
    if archivo:
        os.remove(archivo.filepath)
        db.session.delete(archivo)
        db.session.commit()
        return True
    return False

def conseguir_archivos_de_empleado(id_empleado):
    return Archivo.query.filter_by(empleado_id=id_empleado).all()