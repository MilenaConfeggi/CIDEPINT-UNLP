from marshmallow import Schema, fields, validates_schema
from .tipoDocumento import TipoDocumentoSchema
from .estado import EstadoSchema
from .cliente import ClienteSchema

class LDSchema(Schema):
    id = fields.Integer(dump_only=True)
    nro_legajo = fields.String(required=True)
    fecha_entrada = fields.DateTime(allow_none=True)
    objetivo = fields.String(required=True)
    es_juridico = fields.Boolean(required=True)
    necesita_facturacion = fields.Boolean(required=True)
    motivo_cancelacion = fields.String(allow_none=True)
    cliente = fields.Nested(ClienteSchema, allow_none=True)
    documento_id = fields.Integer(allow_none=True)
    estado_id = fields.Integer(dump_only=True)
    estado = fields.Nested(EstadoSchema, dump_only=True)

class DocumentoSchema(Schema):
    id = fields.Integer(dump_only=True)
    nombre_documento = fields.String(required=True)
    fecha_creacion = fields.DateTime(required=True)
    estado_id = fields.Integer(required=True)
    tipo_documento_id = fields.Integer(required=True)
    legajo_id = fields.Integer(required=True)
    estado = fields.Nested(EstadoSchema, dump_only=True)
    tipo_documento = fields.Nested(TipoDocumentoSchema, dump_only=True)
    legajo = fields.Nested(LDSchema, dump_only=True)
    
documento_schema = DocumentoSchema()
documentos_schema = DocumentoSchema(many=True)


class PaginationDocumentoSchema(Schema):
    items = fields.Nested(DocumentoSchema, many=True)
    total = fields.Integer()
    page = fields.Integer()
    per_page = fields.Integer()
    
pagination_documento_schema = PaginationDocumentoSchema()