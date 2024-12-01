from models.personal.area import Area
from models.base import db
def get_area(id):
    return db.session.query(Area).filter_by(id=id).first()

def list_legajos():
    return db.session.query(Area).all()