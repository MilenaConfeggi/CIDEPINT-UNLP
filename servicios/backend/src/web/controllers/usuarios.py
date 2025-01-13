from servicios.backend.src.core.config import Config
from flask import jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioUsuario
from servicios.backend.src.web.schemas.usuarios import usuariosSchema, usuarioSchema, rolesSchema, empleadosSchema, empleadoSchema, usuariosConNombreSchema
from servicios.backend.src.web.schemas.area import area_schemas
from servicios.backend.src.web.helpers.auth import is_authenticated, check_permission
from flask_jwt_extended import jwt_required, get_jwt_identity
from administracion.src.core.Empleado import get_empleado

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.get("/")
@jwt_required()
def listar_usuarios():
    if not check_permission("listar_usuarios"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    usuarios_paginated = servicioUsuario.listar_usuarios_paginados(page, per_page)
    data = usuariosSchema.dump(usuarios_paginated.items)
    
    return jsonify({
        'usuarios': data,
        'total': usuarios_paginated.total,
        'pages': usuarios_paginated.pages,
        'current_page': usuarios_paginated.page
    }), 200

@bp.get("/<int:id_area>")
@jwt_required()
def listar_usuarios_de_un_area(id_area):
    if not check_permission("listar_usuarios_de_un_area"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    usuarios = servicioUsuario.listar_jefes_de_area_de_un_area(id_area)
    data = usuariosConNombreSchema.dump(usuarios, many=True)
    return jsonify(data), 200

@bp.get("/roles")
@jwt_required()
def listar_roles():
    if not check_permission("listar_roles"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    roles = servicioUsuario.listar_roles()
    data = rolesSchema.dump(roles, many=True)
    return jsonify(data), 200

@bp.get("/empleados")
@jwt_required()
def listar_empleados():
    if not check_permission("listar_empleados"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    empleados = servicioUsuario.listar_empleados()
    data = empleadosSchema.dump(empleados, many=True)
    return jsonify(data), 200

@bp.get("/areas")
@jwt_required()
def listar_areas():
    print("llegué")
    if not check_permission("listar_areas"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    print("llegué2")
    areas = servicioUsuario.listar_areas()
    data = empleadosSchema.dump(areas, many=True)
    return jsonify(data), 200

@bp.get("/ver_perfil")
@jwt_required()
def ver_perfil():
    if not check_permission("ver_perfil"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    empleado = servicioUsuario.obtener_empleado_por_mail(get_jwt_identity())
    data = empleadoSchema.dump(empleado)
    return jsonify(data), 200

@bp.post("/crear")
@jwt_required()
def crear_usuario():
    if not check_permission("crear_usuario"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    try:
        data = request.get_json()

        if data['mail'] == []:
            return jsonify({"message": "No se ha cargado mail"}), 400

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
@jwt_required()
def borrar_usuario():
    if not check_permission("borrar_usuario"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    data = request.get_json()
    id_usuario = data.get('id')
    try:
        servicioUsuario.eliminar_usuario(id_usuario)
        usuarios = servicioUsuario.listar_usuarios()
        data = usuariosSchema.dump(usuarios, many=True)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 406

@bp.post("/recuperar_contra")
@jwt_required()
def recuperar_contra():
    if not check_permission("recuperar_contra"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    try:
        data = request.get_json()

        if data['mail'] == []:
            return jsonify({"message": "No se ha cargado mail"}), 400

        servicioUsuario.recuperar_contra(data)
        
        return jsonify({"message": "Se envió un mail con una contraseña provisional a la dirección de correo del usuario"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    
@bp.post("/cambiar_jefe_area")
@jwt_required()
def cambiar_jefe_area():
    if not check_permission("cambiar_jefe_area"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    data = request.get_json()
    servicioUsuario.cambiar_jefe_area(data)
    return jsonify({"message": "Se cambió el jefe de área exitosamente"}), 200


