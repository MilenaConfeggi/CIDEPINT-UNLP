from models.base import db
from models.clientes.cliente import Cliente
from models.legajos import Legajo


def create_cliente(data, legajo_id):
    cliente = find_cliente_by_cuit(data.get("cuit"))
    if cliente is None:
        cliente = Cliente(**data)
    else:
        for key, value in data.items():
            if getattr(cliente, key) != value:
                setattr(cliente, key, value)
    legajo = db.session.query(Legajo).filter_by(id=legajo_id).first()
    if legajo is None:
        return None
    cliente.legajos.append(legajo)
    db.session.add(cliente)
    db.session.commit()
    return cliente


def get_cliente(id):
    return db.session.query(Cliente).filter_by(id=id).first()

def list_clientes():
    return db.session.query(Cliente).all()

def find_cliente_by_cuit(cuit):
    return db.session.query(Cliente).filter_by(cuit=cuit).first()