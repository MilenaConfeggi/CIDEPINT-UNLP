from servicios.backend.src.core.config import Config
from flask import jsonify, abort, Blueprint, request, send_from_directory
from servicios.backend.src.core.services import servicioPresupuesto
from servicios.backend.src.web.schemas.presupuesto import presupuestoSchema
from servicios.backend.src.web.schemas.presupuesto import mediosPagoSchema
from servicios.backend.src.web.schemas.stan import stansSchema
from servicios.backend.src.web.helpers.auth import is_authenticated, check_permission
from flask_jwt_extended import jwt_required, get_jwt_identity
from administracion.src.core.Empleado import get_empleado
import os
UPLOAD_FOLDER = os.path.abspath("documentos")

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

@bp.post("/crear/<int:id_legajo>")
def crearPresupuesto(id_legajo):
    data = request.get_json()
    if data['medioDePago'] == []:
        return jsonify({"error": "No se seleccionó medio de pago"}), 400
    data['legajo'] = id_legajo
    servicioPresupuesto.crear_presupuesto_con_stans(data)
    return jsonify({"message": "Presupuesto creado correctamente"}), 200

@bp.get("/ver_documento/<int:id_legajo>")
def obtener_presupuesto(id_legajo):
    directory = os.path.normpath(os.path.join(UPLOAD_FOLDER, "presupuestos", str(id_legajo)))

    # Verifica si el directorio existe
    if not os.path.exists(directory) or not os.path.isdir(directory):
        print("El directorio no existe")
        abort(404, description="El documento no existe, prueba generar uno primero")

    # Filtra los archivos que coinciden con el formato de nombre
    archivos = [f for f in os.listdir(directory) if f.startswith("presupuesto_") and f.endswith(".pdf")]

    # Si no hay archivos que coincidan
    if not archivos:
        print("No hay archivos de presupuesto")
        abort(404, description="No se encontraron documentos de presupuesto para este legajo")

    # Encuentra el archivo más reciente basado en el timestamp
    archivos.sort(reverse=True)  # Ordenar por nombre en orden descendente (timestamps más recientes primero)
    archivo_mas_reciente = archivos[0]

    # Ruta completa al archivo
    file_path = os.path.join(directory, archivo_mas_reciente)

    # Enviar el archivo
    return send_from_directory(directory, archivo_mas_reciente)