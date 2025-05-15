from models.base import db

class STAN(db.Model):
    __tablename__ = 'STAN'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(255), nullable=False)
    precio_pesos = db.Column(db.Float, nullable=True)
    precio_dolares = db.Column(db.Float, nullable=True)
    precio_por_muestra = db.Column(db.Boolean, nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)
    rack = db.Column(db.Integer, nullable=True)
    ensayos = db.relationship('Ensayo', secondary='ensayo_stan', back_populates='stans')
    presupuestos = db.relationship('Presupuesto', secondary='presupuesto_stan', back_populates='stans')