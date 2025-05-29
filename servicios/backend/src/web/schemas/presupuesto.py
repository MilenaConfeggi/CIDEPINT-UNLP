from marshmallow import Schema, fields
from .stan import StanSchema

class PresupuestoSchema(Schema):
    id = fields.Integer(dump_only=True)
    nro_presupuesto = fields.Integer(dump_only=True)
    fecha_carga = fields.Date(required=True)
    precio = fields.Float(required=True)
    medio_de_pago_id = fields.Integer(required=True)
    stans = fields.List(fields.Nested(StanSchema), dump_only=True)

class MedioPagoSchema(Schema):
    id = fields.Integer(dump_only=True)
    medio_de_pago = fields.Str(required=True)
    
presupuestoSchema = PresupuestoSchema()
presupuestosSchema = PresupuestoSchema(many=True)


medioPagoSchema = MedioPagoSchema()
mediosPagoSchema = MedioPagoSchema(many=True)
