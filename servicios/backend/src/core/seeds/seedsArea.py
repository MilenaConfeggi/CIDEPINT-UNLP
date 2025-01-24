from models.personal.area import Area
from models.base import db

def seeds_areas():
    areas = [
        Area(nombre="CIDEPINT", saldo=0),
    ]
    db.session.add_all(areas)
    db.session.commit()