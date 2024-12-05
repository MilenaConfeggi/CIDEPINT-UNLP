from models.base import db
from enum import Enum
from models.compras.compra_fondo import compra_fondo
from models.compras.compra_empleado import compra_empleado
from models.compras.compra_area import compra_area

class estado_compra(Enum):
    RECHAZADA = "Rechazada"
    ACEPTADA = "Aceptada"
    PENDIENTE = "Pendiente"

class Compra(db.Model):
    __tablename__ = 'compras'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    numero_factura = db.Column(db.String(30), nullable=False)
    importe = db.Column(db.Float, nullable=False)
    causa_rechazo = db.Column(db.String(200), nullable=True)
    descripcion = db.Column(db.String(200), nullable=False)
    observaciones = db.Column(db.String(200), nullable=True)
    estado = db.Column(db.Enum(estado_compra), nullable=False)
    id_proveedor = db.Column(db.Integer, db.ForeignKey("proveedores.id"), nullable=False)
    proveedor = db.relationship('Proveedor', back_populates='compras')
    #fondos
    #fondos = db.relationship('Fondo', secondary=compra_fondo, back_populates='compras')

    #empleados
    #empleados = db.relationship('Empleado', secondary=compra_empleado ,back_populates='compras')

    #areas
    #areas = db.relationship('Area', secondary=compra_area, back_populates='compras')

    #solicitante
    #id_empleado = db.Column(db.Integer, db.ForeignKey("empleados.id"), nullable=False)
    #empleado = db.relationship('Empleado', back_populates='compras')