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
    
    cliente = db.relationship('Cliente', back_populates='legajo')
    