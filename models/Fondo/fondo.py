from models.base import db
from models.compras.compra_fondo import compra_fondo

class Fondo(db.Model):
    __tablename__ = 'fondo'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    saldo = db.Column(db.DECIMAL(12,2))
    borrado = db.Column(db.Boolean(), default=False)
    compras = db.relationship('Compra', secondary=compra_fondo, back_populates='fondos')
    #carpeta_id = db.Column(db.Integer, db.ForeignKey('carpetas.id'))
    carpeta = db.relationship('Carpeta', back_populates='fondo',uselist = False)
