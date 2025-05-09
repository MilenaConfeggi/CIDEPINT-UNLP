from models.personal.area import Area
from models.base import db
from decimal import Decimal

def get_area(id):
    return db.session.query(Area).filter_by(id=id).first()

def list_areas():
    return db.session.query(Area).all()
def sumar_saldo_area(id, monto):
    area = get_area(id)
    area.saldo += Decimal(monto)
    db.session.commit()
def restar_saldo_area(id, monto):
    area = get_area(id)
    area.saldo -= monto
    db.session.commit()
def get_area_by_name(nombre):
    return db.session.query(Area).filter_by(nombre=nombre).first()