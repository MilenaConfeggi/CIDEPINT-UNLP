from models.base import db

class Archivo(db.Model):
    __tablename__ = 'archivos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)  # Nombre del archivo
    filepath = db.Column(db.String(255), nullable=False)  # Ruta o URL del archivo

    id_bien = db.Column(db.Integer, db.ForeignKey("bienes.id"), nullable=True)
    bienes = db.relationship('Bien', back_populates='archivos')

    id_carpeta = db.Column(db.Integer, db.ForeignKey("carpetas.id"), nullable=True)
    carpeta = db.relationship('Carpeta', back_populates='archivos')