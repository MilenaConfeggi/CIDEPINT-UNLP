from models.base import db
from models.personal.empleado import Empleado
from models.distribucion.distribucion import Distribucion
from models.empleado_distribucion.empleado_distribucion import Empleado_Distribucion


def create_empleado_distribucion(**kwargs):
    """
    Crea una nueva asociación entre un empleado y una distribución.
    kwargs debe incluir empleado_id y distribucion_id.
    """
    db.session.add(Empleado_Distribucion(**kwargs))
    db.session.commit()
    return True


def get_empleado_distribucion(empleado_id, distribucion_id):
    """
    Obtiene una asociación específica entre un empleado y una distribución.
    """
    return (
        db.session.query(Empleado_Distribucion)
        .filter_by(empleado_id=empleado_id, distribucion_id=distribucion_id))

def get_empleados_by_distribucion(distribucion_id):
    """
    Obtiene todos los empleados asociados a una distribución.
    """
    return db.session.query(Empleado).join(Empleado_Distribucion).filter_by(distribucion_id=distribucion_id).all()