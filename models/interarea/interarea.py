from models.base import db

class Interarea(db.Model):
    __tablename__ = 'interarea'
    id = db.Column(db.Integer, primary_key=True)    
    
    # Atributos
    fecha_creacion = db.Column(db.Date, nullable=False)
    fecha_solicitud_no_firmada = db.Column(db.Date, nullable=True)
    fecha_solicitud_firmada = db.Column(db.Date, nullable=True)
    nombre_solicitud_firmada = db.Column(db.String(255), nullable=True)
    nombre_solicitud_no_firmada = db.Column(db.String(255), nullable=True)
    investigacion = db.Column(db.Boolean, nullable=False)
    nro_interarea = db.Column(db.Integer, nullable=False)
    
    # Relaciones
    legajo_id = db.Column(db.Integer, db.ForeignKey('legajo.id'), nullable=False)
    legajo = db.relationship('Legajo', backref=db.backref('interareas', lazy=True))

    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    area = db.relationship('Area', backref=db.backref('interareas', lazy=True))

    muestra_id = db.Column(db.Integer, db.ForeignKey('muestra.id'), nullable=False)
    muestra = db.relationship('Muestra', backref=db.backref('interareas', lazy=True))
    