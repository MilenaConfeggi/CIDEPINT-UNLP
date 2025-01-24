from models.base import db

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    usuario = db.relationship("Usuario", back_populates="rol")

    rol_permiso = db.relationship("RolPermiso", back_populates="rol")