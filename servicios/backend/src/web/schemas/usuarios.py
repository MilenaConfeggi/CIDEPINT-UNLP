from marshmallow import Schema, fields, ValidationError

class UsuarioSchema(Schema):
    mail = fields.Str(required=True)

    #Me trae el nombre del rol, así no me da el rol completo
    rol = fields.Function(lambda obj: obj.rol.nombre if obj.nombre else None)
    

usuarioSchema = UsuarioSchema()
usuariosSchema = UsuarioSchema(many=True)
