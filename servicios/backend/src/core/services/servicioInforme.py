from models.base import db
from models.documentos.documento import Documento
from models.documentos.estado import Estado
from datetime import datetime

def crear_estado(nombre):
    nuevo_estado = Estado(
        nombre= nombre
    )
    db.session.add(nuevo_estado)
    db.session.commit()
    return nuevo_estado

def crear_documento(data):
    nuevo_documento = Documento(
        nombre_documento=data.get('nombre_documento'),
        fecha_creacion=datetime.now(),
        estado_id=data.get('estado_id'),
        legajo_id= data.get('legajo_id')
    )
    db.session.add(nuevo_documento)
    db.session.commit()
    return nuevo_documento