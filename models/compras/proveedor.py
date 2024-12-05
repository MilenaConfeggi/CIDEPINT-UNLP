from models.base import db

class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id = db.Column(db.Integer, primary_key=True)
    razon_social = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(50), nullable=False)
    compras = db.relationship('Compra', back_populates='proveedor', cascade='all, delete-orphan')