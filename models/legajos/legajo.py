from models.base import db

class Legajo(db.Model):
    __tablename__ = 'legajo'
    id = db.Column(db.Integer, primary_key=True)
    nro_legajo = db.Column(db.String(100))
    fecha_entrada = db.Column(db.DateTime)
    objetivo = db.Column(db.String(100))
    es_juridico = db.Column(db.Boolean)
    necesita_facturacion = db.Column(db.Boolean)
    motivo_cancelacion = db.Column(db.String(100), nullable=True)
    #parte_del_proceso_cancelado = 
    
    cliente = db.relationship('Cliente', back_populates='legajo', uselist=False)
    
    resultado_encuesta = db.relationship('ResultadoEncuesta', back_populates='legajo')
    mail = db.relationship('Mail', back_populates='legajo')
    muestras = db.relationship('Muestra', back_populates='legajo')
    presupuesto_cidepint = db.relationship('Presupuesto', back_populates='legajo')
    documento_id = db.Column(db.Integer, db.ForeignKey('documento.id'), nullable=True)
    documento = db.relationship('Documento', back_populates='legajos')