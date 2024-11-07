from models.base import db

class EnsayoStan(db.Model):
    __tablename__ = 'ensayo_stan'
    ensayo_id = db.Column(db.Integer, db.ForeignKey('ensayo.id'), primary_key=True)
    stan_id = db.Column(db.Integer, db.ForeignKey('STAN.id'), primary_key=True)