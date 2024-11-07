from models.base import db

class Presupuesto(db.Model):
    __tablename__ = 'presupuesto'
    id = db.Column(db.Integer, primary_key=True)
    nro_presupuesto = db.Column(db.Integer, nullable=False)
    fecha_carga = db.Column(db.Date, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    medio_de_pago_id = db.Column(db.Integer, db.ForeignKey('medio_pago.id'), nullable=False)

    stans = db.relationship('STAN', secondary='presupuesto_stan', back_populates='presupuestos')