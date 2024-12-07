from models.base import db
from models.documentos.estado import Estado
from models.documentos.tipo_documento import Tipo_Documento
from models.documentos.documento import Documento

def create_estado(data):
    if find_estado_by_nombre(data['nombre']) is not None:
        return None
    estado = Estado(**data)
    db.session.add(estado)
    db.session.commit()
    return estado

def list_estados():
    return db.session.query(Estado).all()

def find_estado_by_nombre(nombre):
    return db.session.query(Estado).filter_by(nombre=nombre).first()

def listar_tipos_documentos():
    return db.session.query(Tipo_Documento).all()

def get_tipo_documento(id):
    return db.session.query(Tipo_Documento).filter_by(id=id).first()

def get_tipo_documento_nombre(nombre):
    return db.session.query(Tipo_Documento).filter_by(nombre = nombre).first()

def create_tipo_documento(data):
    if get_tipo_documento(data['id']) is not None:
        return None
    tipo_documento = Tipo_Documento(**data)
    db.session.add(tipo_documento)
    db.session.commit()
    return tipo_documento

def get_documento(id):
    return db.session.query(Documento).filter_by(id=id).first()

def find_documento(data):
    query = Documento.query
    query = query.filter_by(nombre_documento=data['nombre_documento'])
    query = query.filter_by(estado_id=data['tipo_documento_id'])
    query = query.filter_by(legajo_id=data['legajo_id'])
    return query.first()

def create_documento(data):
    if find_documento(data) is not None:
        return None
    documento = Documento(**data)
    db.session.add(documento)
    db.session.commit()
    return documento