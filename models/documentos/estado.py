from models.base import db

class Estado(db.Model):
    __tablename__ = 'estado'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    
    legajos = db.relationship('Legajo', back_populates='estado')