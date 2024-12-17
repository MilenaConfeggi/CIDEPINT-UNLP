from models.base import db

class EstadoInterarea(db.Model):
    __tablename__ = 'estadoInterarea'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)