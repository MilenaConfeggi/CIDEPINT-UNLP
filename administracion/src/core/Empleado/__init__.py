from models.personal.empleado import Empleado
from models.base import db
def get_empleado(id):
    return db.session.query(Empleado).filter_by(id=id).first()

def list_empleados():
    return db.session.query(Empleado).all()