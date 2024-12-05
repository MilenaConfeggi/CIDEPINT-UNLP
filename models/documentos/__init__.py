from models.base import db
from models.documentos.estado import Estado

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
