from models.base import db

class Muestra(db.Model):
    __tablename__ = 'muestra'
    id = db.Column(db.Integer, primary_key=True)
    nro_muestra = db.Column(db.Integer, nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    iden_cliente = db.Column(db.String(100), nullable=False)
    terminada = db.Column(db.Boolean, nullable=False)

    legajo_id = db.Column(db.Integer, db.ForeignKey('legajo.id'), nullable=False)
    legajo = db.relationship('Legajo', back_populates='muestras')

    fotos = db.relationship('Foto', back_populates='muestra')