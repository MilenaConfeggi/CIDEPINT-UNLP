from models.base import db
from datetime import datetime, timedelta

class FotoShareToken(db.Model):
    __tablename__ = 'foto_share_token'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False)
    legajo_id = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    creado = db.Column(db.DateTime, default=datetime.utcnow)
    expiracion = db.Column(db.DateTime, nullable=False)

    def expirado(self):
        return datetime.utcnow() > self.expiracion