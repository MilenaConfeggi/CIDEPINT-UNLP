from models.base import db

usuarios_leen_carpeta = db.Table(
  "usuarios_leen",
   db.metadata,
   db.Column('id_carpeta', db.ForeignKey('carpetas.id'), primary_key=True),
   db.Column('id_user', db.ForeignKey('user.id'), primary_key=True),
)

usuarios_editan_carpeta = db.Table(
  "usuarios_editan",
   db.metadata,
   db.Column('id_carpeta', db.ForeignKey('carpetas.id'), primary_key=True),
   db.Column('id_user', db.ForeignKey('user.id'), primary_key=True),
)

class Carpeta(db.Model):
    __tablename__ = 'carpetas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)  # Nombre del archivo
    archivos = db.relationship('Archivo', back_populates='carpeta')
    fecha_ingreso = db.Column(db.Date, default=db.func.now())

    id_padre = db.Column(db.Integer, db.ForeignKey('carpetas.id'), nullable=True)
    padre = db.relationship('Carpeta', back_populates='subcarpetas', remote_side=[id])
    subcarpetas = db.relationship('Carpeta', back_populates='padre', lazy='dynamic')

    usuarios_leen = db.relationship("User", secondary=usuarios_leen_carpeta, back_populates="carpetas_lee")
    usuarios_editan = db.relationship('User', secondary=usuarios_editan_carpeta, back_populates='carpetas_edita')

    id_fondo = db.Column(db.Integer, db.ForeignKey('fondo.id'), nullable=True)
    fondo = db.relationship('Fondo', back_populates='carpeta', uselist=False)