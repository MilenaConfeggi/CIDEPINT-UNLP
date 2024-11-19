from models.base import db

class Documento(db.Model):
    __tablename__ = 'documento'
    id = db.Column(db.Integer, primary_key=True)
    nombre_documento = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)

    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=True) #nullable=True porque el documento puede no tener estado (presupuesto conicet)
    estado = db.relationship('Estado', backref=db.backref('documento', uselist=False))
    legajo_id = db.Column(db.Integer, db.ForeignKey('legajo.id'), nullable=False)
    legajo = db.relationship('Legajo', backref=db.backref('documento', uselist=False))
    #Agrego el tipo de documento (presupuesto, informe, certificado, etc)
    tipo_documento_id = db.Column(db.Integer, db.ForeignKey('tipo_documento.id'), nullable=False)
    tipo_documento = db.relationship('Tipo_Documento', backref=db.backref('documento', uselist=False))