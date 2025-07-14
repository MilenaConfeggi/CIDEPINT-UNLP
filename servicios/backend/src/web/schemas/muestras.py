from marshmallow import Schema, fields

class MuestraSchema(Schema):
    id = fields.Int(dump_only=True)
    nro_muestra = fields.Int(required=True)  # Ahora es requerido y no solo de lectura
    nro_grupo = fields.Int(required=False, allow_none=True)  # Campo opcional
    fecha_ingreso = fields.Date(required=True)
    iden_cliente = fields.Str(required=True)
    terminada = fields.Bool(dump_only=True)
    legajo_id = fields.Int(dump_only=True)

muestraSchema = MuestraSchema()
muestrasSchema = MuestraSchema(many=True)

class FotoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre_archivo = fields.Str(required=True)
    fecha = fields.Date(required=True)
    descripcion = fields.Str(required=False, allow_none=True)
    legajo_id = fields.Int(required=True)  # Añadir legajo_id
    muestra_id = fields.Int(required=False, allow_none=True)  # Permitir None
    muestra = fields.Nested(MuestraSchema, dump_only=True)
    legajo_id = fields.Method("get_legajo_id")  # Solo para dump

    def get_legajo_id(self, obj):
        return obj.muestra.legajo_id if obj.muestra else None

fotoSchema = FotoSchema()
fotosSchema = FotoSchema(many=True)