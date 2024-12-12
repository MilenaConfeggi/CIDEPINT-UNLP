from servicios.backend.src.core.config import Config
from flask import jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioUsuario
from servicios.backend.src.web.schemas.usuarios import usuariosSchema, rolesSchema, empleadosSchema
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

@bp.post("/crear")
def crear_usuario():
    data = request.get_json()

    if data['mail'] == []:
        return jsonify({"message": "No se ha cargado mail"}), 400
    
    if data['contra'] == []:
        return jsonify({"message": "No se ha seleccionado contraseña"}), 400

    if data['rol'] == []:
        return jsonify({"message": "No se ha seleccionado rol"}), 400

    if data['empleado'] == []:
        return jsonify({"message": "No se ha seleccionado empleado"}), 400
    
    if not servicioUsuario.buscar_rol_por_id(data['rol']):
        return jsonify({"message": "Rol inexistente"}), 400
    
    data['rol'] = servicioUsuario.buscar_rol_por_id(data['rol'])

    data['empleado'] = get_empleado(data['empleado'])
    
    servicioUsuario.crear_usuario(data)
    
    return jsonify({"message": "Usuario creado correctamente"}), 200

@bp.post("/delete")
def borrar_usuario():
    try:
        servicioUsuario.eliminar_usuario(id_usuario)
        return jsonify({"info": "Usuario borrado exitosamente"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 406



