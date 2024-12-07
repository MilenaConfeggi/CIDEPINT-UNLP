from marshmallow import Schema, fields, validates_schema

class ClienteSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True)
    cuit = fields.String(required=True)
    telefono = fields.String(required=True)
    celular = fields.String(required=True)
    direccion = fields.String(required=True)
    fecha_nacimiento = fields.DateTime(required=True)
    contacto = fields.String(required=True)
    calle = fields.String(required=True)
    numero = fields.String(required=True)
    localidad = fields.String(required=True)
    codigo_postal = fields.String(required=True)
    piso = fields.String(required=True)
    depto = fields.String(required=True)
    legajo_id = fields.Integer(required=True)
    nombre = fields.String(required=True)

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)