from models.base import db
from models.Fondo.fondo import Fondo

def listar_bienes():

    return Fondo.query.all()


def conseguir_bien_de_id(bien_id):

    return Fondo.query.get(bien_id)