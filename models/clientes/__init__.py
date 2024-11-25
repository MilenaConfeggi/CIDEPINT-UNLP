from models.base import db
from models.clientes.cliente import Cliente


def create_cliente(data):
    db.session.add(Cliente(**data))
    db.session.commit()

def get_cliente(id):
    return db.session.query(Cliente).filter_by(id=id).first()

def list_clientes():
    return db.session.query(Cliente).all()

def find_cliente_by_mail(mail):
    return db.session.query(Cliente).filter_by(email=mail).first()