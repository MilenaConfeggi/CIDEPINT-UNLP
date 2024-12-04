from models.base import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class Archivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)  # Corrected foreign key reference
    nombre = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    ruta = db.Column(db.String(200), nullable=False)
    empleado = db.relationship('Empleado', back_populates='archivos')

    def __init__(self, empleado_id, nombre, tipo, ruta):
        self.empleado_id = empleado_id
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