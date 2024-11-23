from models.base import db

class Bien(db.Model):
    __tablename__ = 'bienes'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    numero_inventario = db.Column(db.String(30), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    institucion = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    motivo_baja = db.Column(db.String(200), nullable=True)
    
    archivos = db.relationship('Archivo', back_populates='bienes')
    #id_area = db.Column(db.Integer, db.ForeignKey("areas.id"), nullable=False)
    #area = db.relationship('Area', back_populates='bienes')