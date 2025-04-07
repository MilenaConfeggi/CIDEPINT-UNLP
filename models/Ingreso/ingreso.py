from models.base import db
from datetime import datetime
class Ingreso(db.Model):
    __tablename__ = 'ingreso'
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.DECIMAL(12,2))
    fecha = db.Column(db.DateTime, default=datetime.now())
    receptor = db.relationship("Fondo")
    receptor_id = db.Column(db.Integer, db.ForeignKey("fondo.id"))

    archivo = db.relationship("Archivo")
    archivo_id = db.Column(db.Integer, db.ForeignKey("archivos.id"), nullable=True)