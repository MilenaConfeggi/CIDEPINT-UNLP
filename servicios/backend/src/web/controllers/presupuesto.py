from servicios.backend.src.core.config import Config
from flask import jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioPresupuesto
from servicios.backend.src.web.schemas.presupuesto import presupuestoSchema
from servicios.backend.src.web.schemas.presupuesto import mediosPagoSchema
from servicios.backend.src.web.schemas.stan import stansSchema
from servicios.backend.src.web.helpers.auth import is_authenticated, check_permission
from flask_jwt_extended import jwt_required, get_jwt_identity
from administracion.src.core.Empleado import get_empleado

bp = Blueprint('presupuestos', __name__, url_prefix='/presupuestos')

@bp.get("/stans")
def listarStans():
    STANS = servicioPresupuesto.listar_stans()
    data = stansSchema.dump(STANS, many=True)
    return jsonify(data), 200

@bp.get("/medios_de_pago")
def listarMediosDePago():
    mp = servicioPresupuesto.listar_medios_de_pago()
    data = mediosPagoSchema.dump(mp, many=True)
    return jsonify(data), 200

@bp.post("/crear")
def crearPresupuesto():
    data = request.get_json()
    servicioPresupuesto.crear_presupuesto_con_stans(data)
    return jsonify(data), 200