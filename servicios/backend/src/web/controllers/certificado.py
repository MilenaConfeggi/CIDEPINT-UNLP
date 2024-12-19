from flask import Blueprint, abort, jsonify, request, send_from_directory
from servicios.backend.src.core.services import servicioCertificado
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
UPLOAD_FOLDER = os.path.abspath("documentos")
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
    if empleados:
        return jsonify(empleados)
    return jsonify({"message": "Aún no se ha realizado la distribución"}), 404

@bp.get("/ver_documento/<int:id_legajo>")
@jwt_required()
def obtener_certificado(id_legajo):
    directory = os.path.normpath(os.path.join(UPLOAD_FOLDER, "certificados", str(id_legajo)))
    filename = "certificado.pdf"
    file_path = os.path.join(directory, filename)
    print(file_path)
    if not os.path.exists(file_path):
        print("No existe")
        abort(404, description="Resource not found")
    return send_from_directory(directory, filename)