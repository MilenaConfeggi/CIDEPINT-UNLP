from models.base import db
from models.legajos.legajo import Legajo



def create_legajo(data):
    db.session.add(Legajo(**data))
    db.session.commit()

def get_legajo(id):
    return db.session.query(Legajo).filter_by(id=id).first()

def list_legajos():
    return db.session.query(Legajo).all()