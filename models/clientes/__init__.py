from models.base import db
from models.clientes.cliente import Cliente


def create_cliente(data, legajo_id):
    cliente = Cliente(**data)
    cliente.legajo_id = legajo_id
    db.session.add(cliente)
    db.session.commit()
    return cliente


def get_cliente(id):
    return db.session.query(Cliente).filter_by(id=id).first()

def list_clientes():
    return db.session.query(Cliente).all()

def find_cliente_by_cuit(cuit):
    return db.session.query(Cliente).filter_by(cuit=cuit).first()