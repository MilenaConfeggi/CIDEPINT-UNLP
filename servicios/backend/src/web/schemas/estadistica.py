from marshmallow import Schema, fields

# Esquema para los ensayos
class EnsayoSchema(Schema):
    nombre = fields.String(required=True)
    cantidad = fields.Integer(required=True)

# Esquema para los legajos
class LegajoSchema(Schema):
    estado = fields.String(required=True)  # Estado del legajo (por ejemplo: informado, en curso, etc.)
    cantidad = fields.Integer(required=True)  # Cantidad de legajos en este estado

class ConformidadSchema(Schema):
    categoria = fields.String(required=True)
    cantidad = fields.Integer(required=True)

# Esquema general para las estadísticas
class EstadisticasSchema(Schema):
    legajos = fields.List(fields.Nested(LegajoSchema), required=True)
    conformidad = fields.List(fields.Nested(ConformidadSchema), required=True)  

# Instancia del esquema para serializar
estadisticas_schema = EstadisticasSchema()
estadisticasEnsayo_schema = EnsayoSchema(many=True)
