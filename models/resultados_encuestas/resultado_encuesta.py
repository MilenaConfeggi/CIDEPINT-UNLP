from models.base import db

class ResultadoEncuesta(db.Model):
    __tablename__ = "resultado_encuesta"
    id = db.Column(db.Integer, primary_key=True)
    como_conocio_cidepint = db.Column(db.String(100), nullable=True)
    precio_del_servicio = db.Column(db.String(100), nullable=True)
    calificacion_general = db.Column(db.String(100), nullable=True)
    atencion_adminstracion = db.Column(db.String(100), nullable=True)
    servicio_ofercido_laboratorio = db.Column(db.String(100), nullable=True)
    resulatdo_del_ensayo = db.Column(db.String(100), nullable=True)
    asesoramiento_brindado = db.Column(db.String(100), nullable=True)
    cumplimiento_de_los_plazos = db.Column(db.String(100), nullable=True)
    sistema_de_pago = db.Column(db.String(100), nullable=True)
    otros = db.Column(db.String(100), nullable=True)
    completado = db.Column(db.Boolean, default=False)
    unique_key = db.Column(db.String(100), unique=True, nullable=False)
    
    legajo_id = db.Column(db.Integer, db.ForeignKey('legajo.id'))
    legajo = db.relationship('Legajo', back_populates='resultado_encuesta')