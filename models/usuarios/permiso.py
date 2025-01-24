from models.base import db

class Permiso(db.Model):
    __tablename__ = "permiso"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    
    rol_permiso = db.relationship("RolPermiso", back_populates="permiso")