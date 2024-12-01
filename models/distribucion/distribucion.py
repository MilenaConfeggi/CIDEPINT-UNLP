from models.base import db

class Distribucion(db.Model):
    __tablename__ = 'distribucion'
    
    id = db.Column(db.Integer, primary_key=True)
    porcentaje_area = db.Column(db.Float, nullable=False,default=40.0)
    porcentaje_empleados = db.Column(db.Float, nullable=False,default=50.0)
    porcentaje_comisiones = db.Column(db.Float, nullable=False,default=19.0)
    monto_a_distribuir = db.Column(db.Float, nullable=False)
    costos = db.Column(db.Float, nullable=False)

    legajo_id = db.Column(db.Integer, db.ForeignKey('legajo.id'))
    legajo = db.relationship('Legajo')

    ganancias_de_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    ganancias_de = db.relationship('Area',foreign_keys=[ganancias_de_id])

    #costos_de_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    #costos_de = db.relationship('Area', foreign_keys=[costos_de_id]) #por defeto cidepint