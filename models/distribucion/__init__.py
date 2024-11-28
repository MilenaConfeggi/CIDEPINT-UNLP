from models.base import db
from models.distribucion.distribucion import Distribucion


def create_distribucion(**kwargs):
    # Comprobamos si ya existe una distribución con el mismo id (puedes ajustar la condición según sea necesario)

    db.session.add(Distribucion(**kwargs))
    db.session.commit()
    return True


def get_distribucion(id):
    # Obtener una distribución por su id
    return db.session.query(Distribucion).filter_by(id=id).first()


def list_distribuciones():
    # Obtener todas las distribuciones
    return db.session.query(Distribucion).all()

def list_distribuciones_by_legajo(legajo_id):
    # Obtener todas las distribuciones de un legajo
    return db.session.query(Distribucion).filter_by(legajo_id=legajo_id).all()

def update_distribucion(id, data):
    # Actualizar una distribución existente por id
    distribucion = get_distribucion(id)
    if distribucion:
        for key, value in data.items():
            setattr(distribucion, key, value)
        db.session.commit()
        return True
    return False


def delete_distribucion(id):
    # Eliminar una distribución por su id
    distribucion = get_distribucion(id)
    if distribucion:
        db.session.delete(distribucion)
        db.session.commit()
        return True
    return False

