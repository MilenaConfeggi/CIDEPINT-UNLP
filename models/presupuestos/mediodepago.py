from models.base import db

class MedioPago(db.Model):
    __tablename__ = 'medio_pago'
    id = db.Column(db.Integer, primary_key=True)
    medio_de_pago = db.Column(db.String(50), nullable=False)