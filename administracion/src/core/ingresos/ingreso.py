from models.base import db
from models.Ingreso.ingreso import Ingreso

def listar_ingresos():

    return Ingreso.query.all()


def conseguir_ingreso_de_id(ingreso_id):

    return Ingreso.query.get(ingreso_id)

def create_ingreso(**kwargs):
    ingreso = Ingreso(**kwargs)
    db.session.add(ingreso)
    db.session.commit()
    return ingreso

def modificar_ingreso(id, **kwargs):
    ingreso = conseguir_ingreso_de_id(id)
    if ingreso:
        for key, value in kwargs.items():
            setattr(ingreso, key, value)
        db.session.commit()
        return ingreso
    return None 

def get_ingresos_del_fondo(fondo_id):
    return Ingreso.query.filter_by(receptor_id=fondo_id).all()
def delete_ingreso(id):
    ingreso = conseguir_ingreso_de_id(id)
    if ingreso:
        db.session.delete(ingreso)
        db.session.commit()
        return True
    return False