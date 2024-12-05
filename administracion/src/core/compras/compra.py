from models.compras.compra import Compra

def listar_compras():
    return Compra.query.all()