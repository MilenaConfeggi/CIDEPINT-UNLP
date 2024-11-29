from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from administracion.src.core.database import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    empleado = db.relationship('Empleado', uselist=False, back_populates='user')

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

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