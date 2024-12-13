from marshmallow import Schema, fields, ValidationError

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    mail = fields.Str(required=True)

    #Me trae el nombre del rol, así no me da el rol completo
    rol = fields.Function(lambda obj: obj.rol.nombre if obj.rol else None)

class RolSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)

class EmpleadoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    apellido = fields.Str(required=True)
    email = fields.Str(required=True)
    usuario_servicio_id = fields.Int(required=True)

usuarioSchema = UsuarioSchema()
usuariosSchema = UsuarioSchema(many=True)

rolSchema = RolSchema()
rolesSchema = RolSchema(many=True)

empleadoSchema = EmpleadoSchema()
empleadosSchema = EmpleadoSchema(many=True)
