from marshmallow import Schema, fields, ValidationError

class MailSchema(Schema):
    id = fields.Int(dump_only=True)
    fecha = fields.Date(dump_only=True)
    nombre_archivo = fields.Str(required=True)
    legajo_id = fields.Int(dump_only=True)
    

mailSchema = MailSchema()
mailsSchema = MailSchema(many=True)
