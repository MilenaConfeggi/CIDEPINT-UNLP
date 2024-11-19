from models.base import db
from models.patrimonio.bien import Bien

def listar_bienes():

    return Bien.query.all()


def conseguir_bien_de_id(bien_id):

    return Bien.query.get(bien_id)


def crear_bien(
    titulo,
    numero_inventario,
    anio,
    institucion,
    descripcion,
):
    nuevo_bien = Bien(
            titulo=titulo,
            numero_inventario=numero_inventario,
            anio=anio,
            institucion=institucion,
            descripcion=descripcion,
            )
    
    db.session.add(nuevo_bien)
    db.session.commit()
    
    return nuevo_bien