from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from administracion.src.core.database import db

class Ausencia(db.Model):
    __tablename__ = 'ausencia'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)  # Corrected foreign key reference
    fecha_desde = db.Column(db.Date, nullable=False)
    fecha_hasta = db.Column(db.Date, nullable=False)
    motivo = db.Column(db.String(200), nullable=False)
    empleado = db.relationship('Empleado', back_populates='ausencias')

    def __init__(self, empleado_id, fecha_desde, fecha_hasta, motivo):
        self.empleado_id = empleado_id
        self.fecha_desde = fecha_desde
        self.fecha_hasta = fecha_hasta
        self.motivo = motivo

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()