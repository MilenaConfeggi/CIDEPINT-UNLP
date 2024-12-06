from marshmallow import Schema, fields

class EnsayoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)

class StanSchema(Schema):
    id = fields.Int(dump_only=True)
    numero = fields.Str(required=True)
    precio_pesos = fields.Float(required=True)
    precio_dolares = fields.Float(required=True)
    precio_por_muestra = fields.Bool(required=True)
    ensayos = fields.List(fields.Nested(EnsayoSchema))

stanSchema = StanSchema()
stansSchema = StanSchema(many=True)