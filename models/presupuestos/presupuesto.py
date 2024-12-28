from models.base import db
from datetime import datetime
from sqlalchemy import event

class Presupuesto(db.Model):
    __tablename__ = 'presupuesto'

    id = db.Column(db.Integer, primary_key=True)
    nro_presupuesto = db.Column(db.Integer, nullable=True, unique=True)

    fecha_creacion = db.Column(db.DateTime, default=datetime.now, nullable=False)

    precio = db.Column(db.Float, nullable=False)
    medio_de_pago_id = db.Column(db.Integer, db.ForeignKey('medio_pago.id'), nullable=True)

    stans = db.relationship('STAN', secondary='presupuesto_stan', back_populates='presupuestos')

    legajo_id = db.Column(db.Integer, db.ForeignKey('legajo.id'))
    legajo = db.relationship('Legajo', back_populates='presupuesto_cidepint')

# Evento para establecer el valor predeterminado de nro_presupuesto
@event.listens_for(Presupuesto, 'after_insert')
def set_nro_presupuesto(mapper, connection, target):
    if target.nro_presupuesto is None:  # Si nro_presupuesto es nulo
        connection.execute(
            db.text(
                "UPDATE presupuesto SET nro_presupuesto = :id WHERE id = :id"
            ),
            {"id": target.id}
        )