from marshmallow import Schema, fields, validates_schema

class TipoDocumentoSchema(Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String(required=True)

tipo_documento_schema = TipoDocumentoSchema()