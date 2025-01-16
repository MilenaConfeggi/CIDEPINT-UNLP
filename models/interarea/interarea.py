from models.base import db

# Tabla intermedia para la relación muestras
muestra_interarea = db.Table(
    'muestra_interarea',
    db.Column('interarea_id', db.Integer, db.ForeignKey('interarea.id'), primary_key=True),
    db.Column('muestra_id', db.Integer, db.ForeignKey('muestra.id'), primary_key=True)
)

class Interarea(db.Model):
    __tablename__ = 'interarea'
    id = db.Column(db.Integer, primary_key=True)

    # Atributos
    fecha_creacion = db.Column(db.Date, nullable=False)
    fecha_solicitud_firmada = db.Column(db.Date, nullable=True)
    nombre_archivo = db.Column(db.String(255), nullable=True)
    investigacion = db.Column(db.Boolean, nullable=False)
    nro_investigacion = db.Column(db.String(40), nullable=True)
    nro_interarea = db.Column(db.String(40), nullable=False)
    resultados = db.Column(db.Text, nullable=True)
    muestra_investigacion = db.Column(db.String(255), nullable=True)

    # Relaciones
    estadoInterarea_id = db.Column(db.Integer, db.ForeignKey('estadoInterarea.id'), nullable=True)
    estadoInterarea = db.relationship('EstadoInterarea', backref=db.backref('interareas', lazy=True))

    legajo_id = db.Column(db.Integer, db.ForeignKey('legajo.id'), nullable=True)
    legajo = db.relationship('Legajo', backref=db.backref('interareas', lazy=True))

    area_solicitante_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    area_solicitante = db.relationship('Area', foreign_keys=[area_solicitante_id], backref=db.backref('interareas_solicitadas', lazy=True))

    area_receptora_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    area_receptora = db.relationship('Area', foreign_keys=[area_receptora_id], backref=db.backref('interareas_recibidas', lazy=True))

    # Relación muchos a muchos con Muestra
    muestras = db.relationship('Muestra', secondary=muestra_interarea, backref=db.backref('interareas', lazy='dynamic'))
