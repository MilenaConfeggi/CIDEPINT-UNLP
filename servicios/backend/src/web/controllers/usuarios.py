from servicios.backend.src.core.config import Config
from flask import jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioUsuario
from servicios.backend.src.web.schemas.usuarios import usuariosSchema, usuarioSchema, rolesSchema, empleadosSchema, empleadoSchema
from servicios.backend.src.web.helpers.auth import is_authenticated, check_permission
from flask_jwt_extended import jwt_required, get_jwt_identity
from administracion.src.core.Empleado import get_empleado

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.get("/")
@jwt_required()
def listar_usuarios():
    if not check_permission("listar_usuarios"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    usuarios = servicioUsuario.listar_usuarios()
    data = usuariosSchema.dump(usuarios, many=True)
    return jsonify(data), 200

@bp.get("/roles")
def listar_roles():
    roles = servicioUsuario.listar_roles()
    data = rolesSchema.dump(roles, many=True)
    return jsonify(data), 200

@bp.get("/empleados")
def listar_empleados():
    empleados = servicioUsuario.listar_empleados()
    data = empleadosSchema.dump(empleados, many=True)
    return jsonify(data), 200

@bp.get("/ver_perfil")
@jwt_required()
def ver_perfil():
    empleado = servicioUsuario.obtener_empleado_por_mail(get_jwt_identity())
    data = empleadoSchema.dump(empleado)
    return jsonify(data), 200

@bp.post("/crear")
def crear_usuario():
    try:
        data = request.get_json()

        if data['mail'] == []:
            return jsonify({"message": "No se ha cargado mail"}), 400
        
        if data['contra'] == []:
            return jsonify({"message": "No se ha seleccionado contraseña"}), 400

        if data['rol'] == []:
            return jsonify({"message": "No se ha seleccionado rol"}), 400
        
        if not servicioUsuario.buscar_rol_por_id(data['rol']):
            return jsonify({"message": "Rol inexistente"}), 400
        
        data['rol'] = servicioUsuario.buscar_rol_por_id(data['rol'])

        servicioUsuario.crear_usuario(data)
        
        return jsonify({"message": "Usuario creado correctamente"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 401

@bp.post("/borrar")
def borrar_usuario():
    data = request.get_json()
    id_usuario = data.get('id')
    try:
        servicioUsuario.eliminar_usuario(id_usuario)
        usuarios = servicioUsuario.listar_usuarios()
        data = usuariosSchema.dump(usuarios, many=True)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 406



