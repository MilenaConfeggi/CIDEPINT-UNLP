from models.base import db
from models.documentos.documento import Documento
from models.documentos.estado import Estado
from models.documentos.tipo_documento import Tipo_Documento
from datetime import datetime

def crear_estado(nombre):
    nuevo_estado = Estado(
        nombre= nombre
    )
    db.session.add(nuevo_estado)
    db.session.commit()
    return nuevo_estado

def crear_tipo_documento(nombre):
    nuevo_tipo = Tipo_Documento(
        nombre= nombre
    )
    db.session.add(nuevo_tipo)
    db.session.commit()
    return nuevo_tipo

def crear_documento(data):
    nuevo_documento = Documento(
        nombre_documento=data.get('nombre_documento'),
        fecha_creacion=datetime.now(),
        estado_id=data.get('estado_id'),
        legajo_id= data.get('legajo_id'),
        tipo_documento_id= data.get('tipo_id')
    )
    db.session.add(nuevo_documento)
    db.session.commit()
    return nuevo_documento

def eliminar_documento(nombre):
    doc = Documento.query.filter_by(Documento.nombre_documento == nombre).first()
    db.session.remove(doc)
    db.session.commit()
