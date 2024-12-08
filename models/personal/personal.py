from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models.base import db
from models.archivos_admin.carpeta import usuarios_leen_carpeta, usuarios_editan_carpeta

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    habilitado = db.Column(db.Boolean, default=True)
    rol = db.Column(db.String(20), nullable=False, default='Personal')
    primer_login = db.Column(db.Boolean, default=True)
    empleado = db.relationship('Empleado', uselist=False, back_populates='user')
    carpetas_lee = db.relationship("Carpeta", secondary=usuarios_leen_carpeta, back_populates="usuarios_leen")
    carpetas_edita = db.relationship("Carpeta", secondary=usuarios_editan_carpeta, back_populates="usuarios_editan")

    def __init__(self, username, password, rol='Personal', habilitado=True):
        self.username = username
        self.set_password(password)
        self.rol = rol
        self.habilitado = habilitado

    def __repr__(self) -> str:
        return f"User {self.username}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates('rol')
    def validate_rol(self, key, value):
        allowed_roles = ['Colaborador', 'Administrador', 'Personal']
        if value not in allowed_roles:
            raise ValueError(f"Rol '{value}' no es válido. Debe ser uno de {allowed_roles}.")
        return value
    
    def save(self) -> tuple:
        try:
            db.session.add(self)
            db.session.commit()
            return True, "Usuario creado con éxito"
        except IntegrityError:
            db.session.rollback()
            return False, "El nombre de usuario ya existe."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error en la base de datos: {str(e)}"

    def update(self) -> tuple:
        try:
            db.session.commit()
            return True, "Usuario actualizado con éxito"
        except IntegrityError:
            db.session.rollback()
            return False, "El nombre de usuario ya existe."
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