from marshmallow import Schema, fields, validates_schema
from .tipoDocumento import TipoDocumentoSchema
from .estado import EstadoSchema
from .cliente import ClienteSchema
from .presupuesto import PresupuestoSchema
from .area import AreaSchema

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
    area_id = fields.Integer(attribute="area_id", dump_only=True)
    area = fields.Nested(AreaSchema, dump_only=True)
    presupuesto_cidepint = fields.List(fields.Nested(PresupuestoSchema, dump_only=True, allow_none=True))

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
    total = fields.Integer(dump_only=True)  
    pages = fields.Integer(dump_only=True)  
    current_page = fields.Integer(dump_only=True) 
    per_page = fields.Integer(dump_only=True)  
    
pagination_documento_schema = PaginationDocumentoSchema()