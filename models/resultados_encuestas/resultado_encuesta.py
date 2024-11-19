from models.base import db

class ResultadoEncuesta(db.Model):
    __tablename__ = "resultado_encuesta"
    id = db.Column(db.Integer, primary_key=True)
    como_conocio_cidepint = db.Column(db.String(100))
    precio_del_servicio = db.Column(db.String(100))
    