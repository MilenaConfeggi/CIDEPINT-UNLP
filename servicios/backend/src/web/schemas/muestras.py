from marshmallow import Schema, fields

class MuestraSchema(Schema):
    id = fields.Int(dump_only=True)
    nro_muestra = fields.Int(dump_only=True)
    fecha_ingreso = fields.Date(required=True)
    iden_cliente = fields.Str(required=True)
    legajo_id = fields.Int(dump_only=True)

muestraSchema = MuestraSchema()
muestrasSchema = MuestraSchema(many=True)