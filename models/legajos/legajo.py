from models.base import db

class Legajo(db.Model):
    __tablename__ = 'legajo'
    id = db.Column(db.Integer, primary_key=True)