from models.base import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50), nullable=False)
    contra = db.Column(db.String(100), nullable=False)
    system_admin = db.Column(db.Boolean, default=False, nullable=False)
    esta_borrado = db.Column(db.Boolean, default=False, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now, nullable=False)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    cambiar_contra = db.Column(db.Boolean, default=True, nullable=False)

    rol_id = db.Column(db.Integer, db.ForeignKey("rol.id"), nullable=False)
    rol = db.relationship("Rol", back_populates="usuario")

    empleado = db.relationship("Empleado", back_populates="usuario_servicio")
    
    def __repr__(self):
        return f"<Usuario {self.mail}>"
