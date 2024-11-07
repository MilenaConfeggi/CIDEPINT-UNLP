from models.base import db

class STAN(db.Model):
    __tablename__ = 'STAN'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    precio = db.Column(db.Float, nullable=False)

    ensayos = db.relationship('Ensayo', secondary='ensayo_stan', back_populates='stans')
    presupuestos = db.relationship('Presupuesto', secondary='presupuesto_stan', back_populates='stans')