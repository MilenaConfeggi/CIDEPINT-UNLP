from marshmallow import Schema, fields

class MuestraSchema(Schema):
    id = fields.Int(dump_only=True)
    nro_muestra = fields.Int(dump_only=True)
    fecha_ingreso = fields.Date(required=True)
    iden_cliente = fields.Str(required=True)
    terminada = fields.Bool(dump_only=True)
    legajo_id = fields.Int(dump_only=True)

muestraSchema = MuestraSchema()
muestrasSchema = MuestraSchema(many=True)

class FotoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre_archivo = fields.Str(required=True)
    muestra_id = fields.Int(dump_only=True)
    fecha = fields.Date(required=True)

fotoSchema = FotoSchema()
fotosSchema = FotoSchema(many=True)