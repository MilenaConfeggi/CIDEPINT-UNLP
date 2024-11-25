import os
from werkzeug.utils import secure_filename
from models.base import db
from models.patrimonio.bien import Bien
from models.archivos_admin.archivo import Archivo
from flask import current_app
from administracion.src.core.servicios import archivos_admin as servicio_archivos

def listar_bienes():

    return Bien.query.all()


def conseguir_bien_de_id(id_bien):

    return Bien.query.get(id_bien)


def crear_bien(
    titulo,
    numero_inventario,
    anio,
    institucion,
    descripcion,
):
    nuevo_bien = Bien(
            titulo=titulo,
            numero_inventario=numero_inventario,
            anio=anio,
            institucion=institucion,
            descripcion=descripcion,
            )
    
    db.session.add(nuevo_bien)
    db.session.commit()
    
    return nuevo_bien


def filtrar_bienes(titulo, numero_inventario, area, baja, page, per_page):
    query = Bien.query

    if titulo:
        query = query.filter(Bien.titulo.ilike(f"{titulo}%"))
    if numero_inventario:
        query = query.filter(Bien.numero_inventario.ilike(f"{numero_inventario}%"))
    #if area:
        #query = query.filter(Bien.area_id == area)
    if baja == 'Activos':
        query = query.filter(Bien.motivo_baja == None)
    else:
        query = query.filter(Bien.motivo_baja != None)
    
    return query.order_by(Bien.titulo.asc()).paginate(page=page,per_page=per_page,error_out=False)


def dar_de_baja_bien(id_bien,motivo_baja):
    bien = conseguir_bien_de_id(id_bien)
    bien.motivo_baja=motivo_baja
    
    db.session.commit()
    
    return bien


def restaurar_bien(id_bien):
    bien = conseguir_bien_de_id(id_bien)
    bien.motivo_baja=None
    
    db.session.commit()
    
    return bien


def conseguir_directorio(id_bien):
    bien = conseguir_bien_de_id(id_bien)
    return os.path.join(current_app.root_path,'archivos',bien.titulo)


def guardar_archivos_de_bien(id_bien, archivos):

    for archivo in archivos:
        nombre = secure_filename(archivo.filename)
        directorio = conseguir_directorio(id_bien)

        if not os.path.exists(directorio):
            os.makedirs(directorio)

        nombre = servicio_archivos.generar_nombre_unico(directorio, nombre)
        filepath = os.path.join(directorio, nombre)
        archivo.save(filepath)

        bien = conseguir_bien_de_id(id_bien)

        nuevo_archivo = Archivo(nombre=nombre, bien=bien, filepath=filepath)

        db.session.add(nuevo_archivo)

    db.session.commit()


def editar_bien(
    id_bien,
    titulo,
    numero_inventario,
    anio,
    institucion,
    descripcion,
):
    
    bien = conseguir_bien_de_id(id_bien)
    
    bien.titulo = titulo
    bien.numero_inventario = numero_inventario
    bien.anio = anio
    bien.institucion = institucion
    bien.descripcion = descripcion

    db.session.commit()
    
    return bien