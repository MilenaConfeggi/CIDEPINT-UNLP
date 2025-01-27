from models.personal.area import Area
from models.base import db

def seeds_areas():
    areas = [
        Area(nombre="CIDEPINT", saldo=0),
        Area(nombre="Area 2", saldo=2),
        Area(nombre="Area 3", saldo=3),
        Area(nombre="Area 4", saldo=4),
        Area(nombre="Area 5", saldo=5),
        Area(nombre="Area 6", saldo=6),
    ]
    db.session.add_all(areas)
    db.session.commit()