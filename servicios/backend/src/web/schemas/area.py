from marshmallow import Schema, fields, validates_schema

class AreaSchema(Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String(required=True)
    saldo = fields.Float(required=True)

area_schema = AreaSchema()
area_schemas = AreaSchema(many=True)