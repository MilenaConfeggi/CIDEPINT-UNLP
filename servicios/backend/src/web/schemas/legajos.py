from marshmallow import Schema, fields, validates_schema
from .cliente import ClienteSchema
from .estado import EstadoSchema
from .documento import DocumentoSchema
from .presupuesto import PresupuestoSchema
from .area import AreaSchema
from .tipoDocumento import TipoDocumentoSchema

class DLSchema(Schema):
    id = fields.Integer(dump_only=True)
    nombre_documento = fields.String(required=True)
    fecha_creacion = fields.DateTime(required=True)
    estado_id = fields.Integer(required=True)
    tipo_documento_id = fields.Integer(required=True)
    legajo_id = fields.Integer(required=True)
    estado = fields.Nested(EstadoSchema, dump_only=True)
    tipo_documento = fields.Nested(TipoDocumentoSchema, dump_only=True)
    
dl_schema = DLSchema()
dl_schemas = DLSchema(many=True)



class LegajoSchema(Schema):
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
    documento = fields.List(fields.Nested(DLSchema, dump_only=True))
    area = fields.Nested(AreaSchema, dump_only=True)
    presupuesto_cidepint = fields.List(fields.Nested(PresupuestoSchema, dump_only=True, allow_none=True))

legajo_schema = LegajoSchema()
legajos_schema = LegajoSchema(many=True)

class PaginationLegajosSchema(Schema):
    total = fields.Integer(dump_only=True)  
    pages = fields.Integer(dump_only=True)  
    current_page = fields.Integer(dump_only=True) 
    per_page = fields.Integer(dump_only=True)  
    items = fields.List(fields.Nested(LegajoSchema)) 
    
pagination_legajos_schema = PaginationLegajosSchema()

