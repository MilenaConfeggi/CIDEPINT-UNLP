from models.base import db
from sqlalchemy.orm import Session
from sqlalchemy import event, func
INITIAL_ID = 33
class Legajo(db.Model):
    __tablename__ = 'legajo'
    id = db.Column(db.Integer, primary_key=True)
    nro_legajo = db.Column(db.String(100))
    fecha_entrada = db.Column(db.DateTime)
    objetivo = db.Column(db.String(100))
    es_juridico = db.Column(db.Boolean)
    necesita_facturacion = db.Column(db.Boolean)
    motivo_cancelacion = db.Column(db.String(100), nullable=True)
    parte_del_proceso_cancelado = db.Column(db.String(100), nullable=True)
    
    cliente = db.relationship('Cliente', back_populates='legajo', uselist=False)
    
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'))
    estado = db.relationship('Estado', back_populates='legajos', uselist=False)
    
    resultado_encuesta = db.relationship('ResultadoEncuesta', back_populates='legajo')
    mail = db.relationship('Mail', back_populates='legajo')
    muestras = db.relationship('Muestra', back_populates='legajo')
    presupuesto_cidepint = db.relationship('Presupuesto', back_populates='legajo')
    
    documento = db.relationship('Documento', back_populates='legajo')
    
@event.listens_for(Legajo, "before_insert")
def set_custom_id(mapper, connection, target):
    session = Session.object_session(target)
    last_id = session.query(func.max(Legajo.id)).scalar()
    
    if last_id is None:
        target.id = INITIAL_ID  # Usar el ID global
    else:
        target.id = last_id + 1