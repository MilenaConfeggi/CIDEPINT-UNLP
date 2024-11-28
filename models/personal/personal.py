from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from administracion.src.core.database import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    area = db.relationship('Area', backref=db.backref('users', lazy=True))
    dni = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    dependencia = db.Column(db.String(50), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    subdivision_cargo = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    domicilio = db.Column(db.String(200), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    habilitado = db.Column(db.Boolean, default=True)
    rol = db.Column(db.String(20), nullable=False, default='Personal')
    primer_login = db.Column(db.Boolean, default=True)
    archivos = db.relationship('Archivo', backref='user', lazy=True)
    ausencias = db.relationship('Ausencia', back_populates='empleado')

    @validates('area_id')
    def validate_area(self, key, value):
        if not value:
            raise ValueError("El área no puede estar vacía.")
        return value

    @validates('dependencia')
    def validate_dependencia(self, key, value):
        allowed_dependencias = ['UNLP', 'CIC', 'CONICET']
        if value not in allowed_dependencias:
            raise ValueError(f"Dependencia '{value}' no es válida. Debe ser una de {allowed_dependencias}.")
        return value

    @validates('cargo')
    def validate_cargo(self, key, value):
        allowed_cargos = ['Investigador', 'CPA', 'Administrativo', 'Técnico']
        if value not in allowed_cargos:
            raise ValueError(f"Cargo '{value}' no es válido. Debe ser uno de {allowed_cargos}.")
        return value

    @validates('subdivision_cargo')
    def validate_subdivision_cargo(self, key, value):
        allowed_subdivisiones = {
            'Investigador': ['Asistente', 'Adjunto', 'Independiente', 'Principal', 'Superior'],
            'CPA': ['Profesional Principal', 'Profesional Adjunto', 'Profesional Asistente'],
            'Técnico': ['Profesional', 'Asociado', 'Asistente', 'Auxiliar'],
            'Administrativo': ['ART 9', 'Ley 10430']
        }
        if self.cargo not in allowed_subdivisiones or value not in allowed_subdivisiones[self.cargo]:
            raise ValueError(f"Subdivisión de cargo '{value}' no es válida para el cargo '{self.cargo}'.")
        return value

    @validates('rol')
    def validate_rol(self, key, value):
        allowed_roles = ['Colaborador', 'Administrador', 'Personal']
        if value not in allowed_roles:
            raise ValueError(f"Rol '{value}' no es válido. Debe ser uno de {allowed_roles}.")
        return value

    def __init__(self, username, password, email, area_id, dni, nombre, apellido, dependencia, cargo, subdivision_cargo, telefono=None, domicilio=None, fecha_nacimiento=None, observaciones=None, habilitado=True, rol='Personal'):
        self.username = username
        self.set_password(password)
        self.email = email
        self.area_id = area_id
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.dependencia = dependencia
        self.cargo = cargo
        self.subdivision_cargo = subdivision_cargo
        self.telefono = telefono
        self.domicilio = domicilio
        self.fecha_nacimiento = fecha_nacimiento
        self.observaciones = observaciones
        self.habilitado = habilitado
        self.rol = rol
        self.primer_login = True

    def __repr__(self) -> str:
        return f"User {self.username}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self) -> tuple:
        try:
            db.session.add(self)
            db.session.commit()
            return True, "Usuario creado con éxito"
        except IntegrityError:
            db.session.rollback()
            return False, "El nombre de usuario, email o DNI ya existe."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error en la base de datos: {str(e)}"

    def update(self) -> tuple:
        try:
            db.session.commit()
            return True, "Usuario actualizado con éxito"
        except IntegrityError:
            db.session.rollback()
            return False, "El nombre de usuario, email o DNI ya existe."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error en la base de datos: {str(e)}"

    def delete(self) -> tuple:
        try:
            db.session.delete(self)
            db.session.commit()
            return True, "Usuario eliminado con éxito"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error en la base de datos: {str(e)}"