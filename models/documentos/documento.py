from models.base import db
from datetime import datetime

class Documento(db.Model):
    __tablename__ = 'documento'
    id = db.Column(db.Integer, primary_key=True)
    nombre_documento = db.Column(db.String(100), nullable=False)
    fecha_carga = db.Column(db.DateTime, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    
    legajos = db.relationship('Legajo', back_populates='documento')
