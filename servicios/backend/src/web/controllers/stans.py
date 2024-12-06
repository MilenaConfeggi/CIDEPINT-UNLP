from servicios.backend.src.core.services import servicioPresupuesto
from flask import Blueprint, jsonify, abort, request, send_file, send_from_directory
from servicios.backend.src.web.schemas.stan import stansSchema, stanSchema, ensayoSchema, EnsayosSchema

bp = Blueprint('stans', __name__, url_prefix='/stans')

@bp.get("/")
def listar_stans():
    stans = servicioPresupuesto.listar_stans()
    data = stansSchema.dump(stans)
    return jsonify(data), 200

@bp.post("/subir_stan")
def cargar_stan():
    data = request.get_json()
    print(data)

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