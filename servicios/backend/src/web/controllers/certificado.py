from flask import Blueprint, jsonify, request
from servicios.backend.src.core.services import servicioCertificado
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("certificado", __name__, url_prefix="/certificado")

@bp.post("/crear/<int:id_legajo>")
@jwt_required()
def crear_certificado(id_legajo):
    data = request.get_json()
    empleados = data.get('empleados', [])
    servicioCertificado.generar_certificado(id_legajo, empleados)
    return jsonify({"message": "Certificado generado"})


@bp.get("/obtener_empleados/<int:id_legajo>")
@jwt_required()
def obtener_empleados(id_legajo):
    empleados = servicioCertificado.obtener_empleados(id_legajo)
    return jsonify(empleados)