from models.base import db
'''
class usuarios_lee_carpetas(db.Model):
    __tablename__ = 'usuarios_lee_carpetas'
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    id_carpeta = db.Column(db.Integer, db.ForeignKey('carpetas.id'), primary_key=True)

class usuarios_edita_carpetas(db.Model):
    __tablename__ = 'usuarios_edita_carpetas'
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    id_carpeta = db.Column(db.Integer, db.ForeignKey('carpetas.id'), primary_key=True)
'''

class Carpeta(db.Model):
    __tablename__ = 'carpetas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)  # Nombre del archivo
    archivos = db.relationship('Archivo', back_populates='carpeta')

    #usuarios_lee = db.relationship('Usuario', secondary='usuarios_lee_carpetas', back_populates='carpetas_lee')
    #usuarios_edita = db.relationship('Usuario', secondary='usuarios_edita_carpetas', back_populates='carpetas_edita')