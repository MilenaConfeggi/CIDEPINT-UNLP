from servicios.backend.src.core.services import servicioPresupuesto
from flask import Blueprint, jsonify, abort, request, send_file, send_from_directory
from servicios.backend.src.web.schemas.stan import stansSchema, stanSchema, ensayoSchema, EnsayosSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from web.helpers.auth import is_authenticated, check_permission
bp = Blueprint('stans', __name__, url_prefix='/stans')

@bp.route("/", methods=["GET"])
@jwt_required()
def listar_stans():
    if not check_permission("listar_stans"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    current_user = get_jwt_identity()
    print(current_user)
    stans = servicioPresupuesto.listar_stans()  
    data = stansSchema.dump(stans)  
    return jsonify(data), 200

@bp.post("/subir_stan")
def cargar_stan():
    data = request.get_json()

    if data['ensayos'] == []:
        return jsonify({"message": "No se han cargado ensayos"}), 400
    
    stan = servicioPresupuesto.crear_stan(data)
    if stan is None:
        return jsonify({"message": "El stan ya existe"}), 400
    
    for ensayo in data['ensayos']:
        print(ensayo)
        ensayo = servicioPresupuesto.crear_ensayo(ensayo)
        servicioPresupuesto.crear_ensayo_stan(ensayo.id, stan.id)
    return jsonify({"message": "Stan cargado correctamente"}), 200

@bp.get("/ensayos")
def listar_ensayos():
    ensayos = servicioPresupuesto.listar_ensayos()
    data = EnsayosSchema.dump(ensayos)
    return jsonify(data), 200

@bp.get("/modificar_stan/<int:id>")
def modificar_stan(id):
    stan = servicioPresupuesto.buscar_stan(id)
    if stan is None:
        return jsonify({"message": "El stan no existe"}), 400
    data = stanSchema.dump(stan)
    return jsonify(data), 200

@bp.post("/editar_stan/<int:id>")
def editar_stan(id):
    data = request.get_json()
    stan = servicioPresupuesto.buscar_stan(id)
    if stan is None:
        return jsonify({"message": "El stan no existe"}), 400
    servicioPresupuesto.modificar_precio_stan(id, data)
    return jsonify({"message": "Stan modificado correctamente"}), 200