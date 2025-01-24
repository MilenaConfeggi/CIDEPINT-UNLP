from models.base import db
from models.personal.area import Area


def list_areas():
    return db.session.query(Area).all()

def get_area(id):
    return db.session.query(Area).filter_by(id=id).first()