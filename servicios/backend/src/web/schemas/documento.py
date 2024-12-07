from marshmallow import Schema, fields, validates_schema
from .tipoDocumento import TipoDocumentoSchema
from .estado import EstadoSchema

class DocumentoSchema(Schema):
    id = fields.Integer(dump_only=True)
    nombre_documento = fields.String(required=True)
    fecha_creacion = fields.DateTime(required=True)
    estado_id = fields.Integer(required=True)
    tipo_documento_id = fields.Integer(required=True)
    legajo_id = fields.Integer(required=True)
    estado = fields.Nested(EstadoSchema, dump_only=True)
    tipo_documento = fields.Nested(TipoDocumentoSchema, dump_only=True)
    
documento_schema = DocumentoSchema()
documentos_schema = DocumentoSchema(many=True)