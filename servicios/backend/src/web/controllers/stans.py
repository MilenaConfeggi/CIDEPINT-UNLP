from servicios.backend.src.core.services import servicioPresupuesto
from flask import Blueprint, jsonify, abort, request, send_file, send_from_directory
from servicios.backend.src.web.schemas.stan import stansSchema, stanSchema

bp = Blueprint('stans', __name__, url_prefix='/stans')

@bp.get("/")
def listar_stans():
    stans = servicioPresupuesto.listar_stans()
    data = stansSchema.dump(stans)
    return jsonify(data), 200