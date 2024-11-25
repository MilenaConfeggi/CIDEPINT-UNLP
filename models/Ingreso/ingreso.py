from models.base import db
from datetime import datetime
class Ingreso(db.Model):
    __tablename__ = 'ingreso'
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float)
    fecha = db.Column(db.DateTime, default=datetime.now())
    receptor = db.relationship("Fondo")
    receptor_id = db.Column(db.String(100), db.ForeignKey("fondo.titulo"))