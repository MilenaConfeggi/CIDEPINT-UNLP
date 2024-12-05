from models.base import db

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    cuit = db.Column(db.String(100),)
    telefono = db.Column(db.String(100))
    celular = db.Column(db.String(100), nullable=True)
    direccion = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.DateTime)
    contacto = db.Column(db.String(100))
    calle = db.Column(db.String(100))
    numero = db.Column(db.String(100))
    localidad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(100))
    piso = db.Column(db.String(100), nullable=True)
    depto = db.Column(db.String(100), nullable=True)
    
    legajo_id = db.Column(db.Integer, db.ForeignKey('legajo.id'))
    legajo = db.relationship('Legajo', back_populates='cliente')