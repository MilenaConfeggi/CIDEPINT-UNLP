from models.base import db

class Foto(db.Model):
    __tablename__ = 'foto'
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    muestra_id = db.Column(db.Integer, db.ForeignKey('muestra.id'))
    muestra = db.relationship('Muestra', back_populates='fotos')