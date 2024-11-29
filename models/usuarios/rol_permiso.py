from models.base import db

class Rol(db.Model):
    __tablename__ = 'rol_permiso'
    rol_id = db.Column(db.Integer, db.ForeignKey("rol.id"), primary_key=True)
    rol = db.relationship("Rol", back_populates="rol_permiso")

    permiso_id = db.Column(
        db.Integer, db.ForeignKey("permiso.id"), primary_key=True
    )
    permiso = db.relationship("Permiso", back_populates="rol_permiso")