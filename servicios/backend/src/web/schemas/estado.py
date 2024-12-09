from marshmallow import Schema, fields, validates_schema

class EstadoSchema(Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String(required=True)

estado_schema = EstadoSchema()
estados_schema = EstadoSchema(many=True)