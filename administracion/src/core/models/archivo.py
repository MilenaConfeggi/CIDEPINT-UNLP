from src.core.database import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class Archivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    ruta = db.Column(db.String(200), nullable=False)

    def __init__(self, user_id, nombre, tipo, ruta):
        self.user_id = user_id
        self.nombre = nombre
        self.tipo = tipo
        self.ruta = ruta

    def __repr__(self) -> str:
        return f"Archivo {self.nombre}"

    def save(self) -> tuple:
        try:
            db.session.add(self)
            db.session.commit()
            return True, "Archivo guardado con éxito"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error en la base de datos: {str(e)}"

    def delete(self) -> tuple:
        try:
            db.session.delete(self)
            db.session.commit()
            return True, "Archivo eliminado con éxito"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error en la base de datos: {str(e)}"