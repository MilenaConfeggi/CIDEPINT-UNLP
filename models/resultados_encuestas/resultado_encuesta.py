from models.base import db

class ResultadoEncuesta(db.Model):
    __tablename__ = "resultado_encuesta"
    id = db.Column(db.Integer, primary_key=True)
    como_conocio_cidepint = db.Column(db.String(100))
    precio_del_servicio = db.Column(db.String(100))
    calificacion_general = db.Column(db.String(100))
    atencion_adminstracion = db.Column(db.String(100))
    servicio_ofercido_laboratorio = db.Column(db.String(100))
    resulatdo_del_ensayo = db.Column(db.String(100))
    asesoramiento_brindado = db.Column(db.String(100))
    cumplimiento_de_los_plazos = db.Column(db.String(100))
    sistema_de_pago = db.Column(db.String(100))
    
    legajo_id = db.Column(db.Integer, db.ForeignKey('legajo.id'))
    legajo = db.relationship('Legajo', back_populates='resultado_encuesta')