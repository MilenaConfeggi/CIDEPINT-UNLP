from models.personal.area import Area
from models.base import db

def seeds_areas():
    areas = [
        Area(nombre="Area 1", saldo=10000),
        Area(nombre="Area 2", saldo=20000),
        Area(nombre="Area 3", saldo=30000),
    ]
    db.session.add_all(areas)
    db.session.commit()