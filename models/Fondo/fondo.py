from models.base import db
from models.compras.compra_fondo import compra_fondo

class Fondo(db.Model):
    __tablename__ = 'fondo'
    titulo = db.Column(db.String(100), primary_key=True)
    saldo = db.Column(db.Float)
    borrado = db.Column(db.Boolean(), default=False)
    compras = db.relationship('Compra', secondary=compra_fondo, back_populates='fondos')
