from marshmallow import Schema, fields, ValidationError
class AreaSchema(Schema):
    id = fields.Int()
    nombre = fields.Str()
class EmpleadoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    apellido = fields.Str(required=True)
    email = fields.Str(required=True)
    usuario_servicio_id = fields.Int(required=True)
    area = fields.Nested(AreaSchema)

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    mail = fields.Str(required=True)
    rol = fields.Function(lambda obj: obj.rol.nombre if obj.rol else None)
    empleado = fields.Nested(EmpleadoSchema)

    #Me trae el nombre del rol, así no me da el rol completo
    rol = fields.Function(lambda obj: obj.rol.nombre if obj.rol else None)

class UsuarioConNombreSchema(Schema):
    id = fields.Int(dump_only=True)
    mail = fields.Str(required=True)

    #Me trae el nombre del rol, así no me da el rol completo
    rol = fields.Function(lambda obj: obj.rol.nombre if obj.rol else None)

    nombre = fields.Function(lambda obj: obj.empleado.nombre if obj.empleado else None)
    apellido = fields.Function(lambda obj: obj.empleado.apellido if obj.empleado else None)

class RolSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)



usuarioSchema = UsuarioSchema()
usuariosSchema = UsuarioSchema(many=True)

usuarioConNombreSchema = UsuarioConNombreSchema()
usuariosConNombreSchema = UsuarioConNombreSchema(many=True)

rolSchema = RolSchema()
rolesSchema = RolSchema(many=True)

areaSchema = AreaSchema()
areasSchema = AreaSchema(many=True)

empleadoSchema = EmpleadoSchema()
empleadosSchema = EmpleadoSchema(many=True)
