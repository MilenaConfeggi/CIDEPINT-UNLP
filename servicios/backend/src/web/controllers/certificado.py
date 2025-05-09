from flask import Blueprint, abort, jsonify, request, send_from_directory
from servicios.backend.src.core.services import servicioCertificado
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.legajos import end_legajo
import os

UPLOAD_FOLDER = os.path.abspath("documentos")
bp = Blueprint("certificado", __name__, url_prefix="/certificado")

@bp.post("/crear/<int:id_legajo>")
@jwt_required()
def crear_certificado(id_legajo):
    data = request.get_json()
    empleados = data.get('empleados', [])
    descripcion = data.get('descripcion', None)
    if servicioCertificado.calcular_suma_participacion(empleados) != 100:
        return jsonify({"message": "La suma de las participaciones debe ser 100"}), 400
    if servicioCertificado.chequear_solo_responsable(empleados) != 1:
        return jsonify({"message": "Debe haber un responsable de equipo"}), 400
    servicioCertificado.generar_certificado(id_legajo, empleados, descripcion)
    end_legajo(id_legajo)
    return jsonify({"message": "Certificado generado"})


@bp.get("/ver_documento/<int:id_legajo>")
@jwt_required()
def obtener_certificado(id_legajo):
    directory = os.path.normpath(os.path.join(UPLOAD_FOLDER, "certificados", str(id_legajo)))
    filename = "certificado.pdf"
    file_path = os.path.join(directory, filename)
    print(file_path)
    if not os.path.exists(file_path):
        print("No existe")
        abort(404, description="El documento no existe, prueba generar uno primero")
    return send_from_directory(directory, filename)

@bp.get("/chequear_descripcion_existente/<int:id_legajo>")
@jwt_required()
def chequear_descripcion_existente(id_legajo):
    descripcion = servicioCertificado.chequear_descripcion_existente(id_legajo)
    print(descripcion)
    if descripcion:
        return jsonify(descripcion)
    return jsonify({"message": "No se encontró la descripción"}), 404