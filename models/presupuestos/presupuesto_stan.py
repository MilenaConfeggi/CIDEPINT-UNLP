from models.base import db

class PresupuestoStan(db.Model):
    __tablename__ = 'presupuesto_stan'
    presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuesto.id'), primary_key=True)
    stan_id = db.Column(db.Integer, db.ForeignKey('STAN.id'), primary_key=True)
    precio_carga = db.Column(db.Float, nullable=False)