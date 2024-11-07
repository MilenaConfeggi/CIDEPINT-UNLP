from models.base import db

class Ensayo(db.Model):
    __tablename__ = 'ensayo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    stans = db.relationship('STAN', secondary='ensayo_stan', back_populates='ensayos')