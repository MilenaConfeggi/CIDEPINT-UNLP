from models.base import db

class Archivo(db.Model):
    __tablename__ = 'archivos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)  # Nombre del archivo
    filepath = db.Column(db.String(255), nullable=False)  # Ruta o URL del archivo
    tipo = db.Column(db.String(50), nullable=True)

    id_bien = db.Column(db.Integer, db.ForeignKey("bienes.id"), nullable=True)
    bien = db.relationship('Bien', back_populates='archivos')

    id_carpeta = db.Column(db.Integer, db.ForeignKey("carpetas.id"), nullable=True)
    carpeta = db.relationship('Carpeta', back_populates='archivos')

    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    empleado = db.relationship('Empleado', back_populates='archivos')