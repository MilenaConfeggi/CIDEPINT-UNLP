from marshmallow import Schema, fields
from .area import AreaSchema
from .legajos import LegajoSchema
from .muestras import MuestraSchema

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
    legajo = fields.Nested(LegajoSchema, dump_only=True)
    area_solicitante = fields.Nested(AreaSchema, dump_only=True)
    area_receptora = fields.Nested(AreaSchema, dump_only=True)
    muestras = fields.Nested(MuestraSchema, many=True, dump_only=True)  # Cambiado para manejar múltiples muestras

interareaSchema = InterareaSchema()
interareasSchema = InterareaSchema(many=True)
