from marshmallow import Schema, fields, ValidationError

class MailSchema(Schema):
    id = fields.Int(dump_only=True)
    fecha = fields.Date(required=True)
    nombre_archivo = fields.Str(required=True)
    legajo_id = fields.Int(required=True)
    

mailSchema = MailSchema()
mailsSchema = MailSchema(many=True)

