from models.base import db
from models.legajos.legajo import Legajo



def create_legajo(data):
    if find_legajo_by_id(data['nro_legajo']):
        return False
    db.session.add(Legajo(**data))
    db.session.commit()
    return True

def get_legajo(id):
    return db.session.query(Legajo).filter_by(id=id).first()

def list_legajos():
    return db.session.query(Legajo).all()

def find_legajo_by_id(nro_legajo):
    return db.session.query(Legajo).filter_by(nro_legajo=nro_legajo).first()