from models.base import db
from models.compras.compra_area import compra_area
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    saldo = db.Column(db.DECIMAL(12,2), nullable=False)

    bienes = db.relationship('Bien', back_populates='area')
    compras = db.relationship('Compra', secondary=compra_area, back_populates='areas')
    
    def __init__(self, nombre, saldo):
        self.nombre = nombre
        self.saldo = saldo

    def __repr__(self) -> str:
        return f"Area {self.nombre}"

    def save(self) -> tuple:
        try:
            db.session.add(self)
            db.session.commit()
            return True, "Área creada con éxito"
        except IntegrityError:
            db.session.rollback()
            return False, "El nombre del área ya existe."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error en la base de datos: {str(e)}"

    def update(self) -> tuple:
        try:
            db.session.commit()
            return True, "Área actualizada con éxito"
        except IntegrityError:
            db.session.rollback()
            return False, "El nombre del área ya existe."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error en la base de datos: {str(e)}"

    def delete(self) -> tuple:
        try:
            db.session.delete(self)
            db.session.commit()
            return True, "Área eliminada con éxito"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error en la base de datos: {str(e)}"