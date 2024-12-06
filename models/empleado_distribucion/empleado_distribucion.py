from models.base import db
class Empleado_Distribucion(db.Model):
    __tablename__ = "empleado_distribucion"

    empleado_id = db.Column(
        db.Integer, db.ForeignKey("empleado.id"), primary_key=True
    )
    distribucion_id = db.Column(
        db.Integer, db.ForeignKey("distribucion.id"), primary_key=True
    )

    empleado = db.relationship("Empleado", back_populates="distribuciones_asociadas")
    distribucion = db.relationship(
        "Distribucion", back_populates="empleados_asociados"
    )
