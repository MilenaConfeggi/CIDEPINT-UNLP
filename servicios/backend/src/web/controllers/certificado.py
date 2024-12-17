from flask import Blueprint, jsonify, request
from servicios.backend.src.core.services import servicioCertificado

bp = Blueprint("certificado", __name__, url_prefix="/certificado")

@bp.get("/crear/<int:id_legajo>")
def crear_certificado(id_legajo):
    servicioCertificado.generar_certificado(id_legajo)
    return jsonify({"message": "Certificado generado"})