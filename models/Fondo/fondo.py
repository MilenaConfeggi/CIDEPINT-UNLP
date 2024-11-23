from models.base import db

class Fondo(db.Model):
    __tablename__ = 'fondo'
    titulo = db.Column(db.String(100), primary_key=True)
    saldo = db.Column(db.Float)
