from marshmallow import Schema, fields

class InterareaSchema(Schema):
    id = fields.Int(dump_only=True)
    fecha_creacion = fields.Date(required=True)
    fecha_solicitud_firmada = fields.Date(required=True)
    nombre_archivo = fields.Str(required=True)
    investigacion = fields.Boolean(required=True)
    nro_investigacion = fields.Str(required=True)  
    nro_interarea = fields.Str(required=True)
    resultados = fields.Str(required=True)
    estadoInterarea_id = fields.Int(dump_only=True)
    legajo_id = fields.Int(dump_only=True)
    area_id = fields.Int(dump_only=True)
    muestra_id = fields.Int(dump_only=True)

interareaSchema = InterareaSchema()
interareasSchema = InterareaSchema(many=True)