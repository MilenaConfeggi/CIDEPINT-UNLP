from servicios.backend.src.core.config import Config
from flask import jsonify, abort, Blueprint, request, send_from_directory
from servicios.backend.src.core.services import servicioPresupuesto, servicioDocumento, servicioUsuario
from servicios.backend.src.web.schemas.presupuesto import presupuestoSchema
from servicios.backend.src.web.schemas.presupuesto import mediosPagoSchema
from servicios.backend.src.web.schemas.stan import stansSchema
from servicios.backend.src.web.helpers.auth import is_authenticated, check_permission
from flask_jwt_extended import jwt_required, get_jwt_identity
from administracion.src.core.Empleado import get_empleado
import os
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = os.path.abspath("documentos")

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}

bp = Blueprint('presupuestos', __name__, url_prefix='/presupuestos')

@bp.get("/stans")
@jwt_required()
def listarStans():
    if not check_permission("listarStans"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    STANS = servicioPresupuesto.listar_stans()
    data = stansSchema.dump(STANS, many=True)
    return jsonify(data), 200

#@bp.get("/medios_de_pago")
#def listarMediosDePago():
#    mp = servicioPresupuesto.listar_medios_de_pago()
#    data = mediosPagoSchema.dump(mp, many=True)
#    return jsonify(data), 200

@bp.post("/crear/<int:id_legajo>")
@jwt_required()
def generar_presupuesto(id_legajo):
    if not check_permission("generar_presupuesto"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    data = request.get_json()
    #if data['medioDePago'] == []:
    #    return jsonify({"error": "No se seleccionó medio de pago"}), 400
    data['legajo'] = id_legajo
    try:
        servicioPresupuesto.crear_presupuesto_con_stans(data)
    except TypeError:
        return jsonify({"message": "Uno de los STANs seleccionados no tiene precio en dólares, cárguele el precio e intente nuevamente"}), 400
    return jsonify({"message": "Presupuesto en dólares creado correctamente"}), 200

@bp.post("/crear_pesos/<int:id_legajo>")
@jwt_required()
def generar_presupuesto_pesos(id_legajo):
    if not check_permission("generar_presupuesto"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    data = request.get_json()
    #if data['medioDePago'] == []:
    #    return jsonify({"error": "No se seleccionó medio de pago"}), 400
    data['legajo'] = id_legajo
    try:
        servicioPresupuesto.crear_presupuesto_con_stans_en_pesos(data)
    except TypeError:
        return jsonify({"message": "Uno de los STANs seleccionados no tiene precio en pesos, cárguele el precio e intente nuevamente"}), 400
    return jsonify({"message": "Presupuesto en pesos creado correctamente"}), 200


@bp.get("/sin_presu/<int:id_legajo>")
@jwt_required()
def buscar_presupuestont(id_legajo):
    if not check_permission("generar_presupuestont"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    #if data['medioDePago'] == []:
    #    return jsonify({"error": "No se seleccionó medio de pago"}), 400
    data = servicioPresupuesto.tiene_presupuestont(id_legajo)
    print(data)
    return jsonify(data), 200

@bp.post("/crearnt/<int:id_legajo>")
@jwt_required()
def generar_presupuestont(id_legajo):
    if not check_permission("generar_presupuestont"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    data = request.get_json()
    #if data['medioDePago'] == []:
    #    return jsonify({"error": "No se seleccionó medio de pago"}), 400
    data['legajo'] = id_legajo
    servicioPresupuesto.crear_presupuestont_con_stans(data)
    return jsonify({"message": "Marcado como sin presupuesto correctamente"}), 200

@bp.get("/ver_documento/<int:id_legajo>")
@jwt_required()
def ver_presupuesto(id_legajo):
    if not check_permission("ver_presupuesto"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    directory = os.path.normpath(os.path.join(UPLOAD_FOLDER, "presupuestos", str(id_legajo)))

    # Verifica si el directorio existe
    if not os.path.exists(directory) or not os.path.isdir(directory):
        print("El directorio no existe")
        abort(404, description="El documento no existe, prueba generar uno primero")

    # Filtra los archivos que coinciden con el formato de nombre
    #PRIORIZO LOS FIRMADOS
    archivos = [f for f in os.listdir(directory) if f.startswith("fpresupuesto_firmado_") and f.endswith(".pdf")]

    if not archivos:
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

@bp.get("/ver_legajo/<int:id_legajo>")
@jwt_required()
def ver_legajo(id_legajo):
    if not check_permission("ver_legajo"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    directory = os.path.normpath(os.path.join(UPLOAD_FOLDER, "legajos", str(id_legajo)))
    print(directory)
    # Verifica si el directorio existe
    if not os.path.exists(directory) or not os.path.isdir(directory):
        print("El directorio no existe")
        abort(404, description="El documento no existe, prueba generar uno primero")

    # Filtra los archivos que coinciden con el formato de nombre
    archivos = [f for f in os.listdir(directory) if f.startswith("legajo_") and f.endswith(".pdf")]

    # Si no hay archivos que coincidan
    if not archivos:
        print("No hay archivos de legajos")
        abort(404, description="No se encontraron documentos de legajo para este legajo")

    # Encuentra el archivo más reciente basado en el timestamp
    archivos.sort(reverse=True)  # Ordenar por nombre en orden descendente (timestamps más recientes primero)
    archivo_mas_reciente = archivos[0]

    # Ruta completa al archivo
    file_path = os.path.join(directory, archivo_mas_reciente)

    # Enviar el archivo
    return send_from_directory(directory, archivo_mas_reciente)

#@bp.get("/ver_documento_firmado/<int:id_legajo>")
#@jwt_required()
#def ver_presupuesto_firmado(id_legajo):
#    if not check_permission("ver_presupuesto_firmado"):
#        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
#    directory = os.path.normpath(os.path.join(UPLOAD_FOLDER, "presupuestos_firmados", str(id_legajo)))

    # Verifica si el directorio existe
#    if not os.path.exists(directory) or not os.path.isdir(directory):
#        print("El directorio no existe")
#        abort(404, description="El documento no existe, prueba generar uno primero")

    # Filtra los archivos que coinciden con el formato de nombre
#    archivos = [f for f in os.listdir(directory) if f.startswith("presupuesto_") and f.endswith(".pdf")]

    # Si no hay archivos que coincidan
#    if not archivos:
#        print("No hay archivos de presupuesto")
#        abort(404, description="No se encontraron documentos de presupuesto para este legajo")

    # Encuentra el archivo más reciente basado en el timestamp
#    archivos.sort(reverse=True)  # Ordenar por nombre en orden descendente (timestamps más recientes primero)
#    archivo_mas_reciente = archivos[0]

    # Ruta completa al archivo
 #   file_path = os.path.join(directory, archivo_mas_reciente)

    # Enviar el archivo
#    return send_from_directory(directory, archivo_mas_reciente)

def permitir_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {"pdf"}

@bp.post("/cargar_presupuesto_firmado/<int:id_legajo>")
@jwt_required()
def cargar_presupuesto_firmado(id_legajo):
    if not check_permission("cargar_presupuesto_firmado"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    if 'archivo' not in request.files:
        return jsonify({"error": "Debes seleccionar un archivo"}), 400

    archivo = request.files['archivo']

    if not archivo or archivo.filename == '':
        return jsonify({"error": "Por favor seleccione un archivo"}), 400

    if not permitir_pdf(archivo.filename):
        return jsonify({"error": "Tipo de archivo no permitido. Solo se permiten archivos PDF o del paquete Office."}), 400
    
    if not servicioPresupuesto.buscar_presupuesto_por_legajo(id_legajo):
        return jsonify({"error": "No hay presupuesto para este legajo"}), 404
    
    try:
        # Eliminar el informe anterior
        #chequeo si quien hizo la peticion es un jefe de area o un director
        user = get_jwt_identity()
        usuario = servicioUsuario.obtener_usuario_por_mail(user)
        if not servicioUsuario.es_director(usuario):
            return jsonify({"error": "No tienes permisos para realizar esta acción"}), 403
        
        folder_path = os.path.join(UPLOAD_FOLDER, "presupuestos", str(id_legajo))
        os.makedirs(folder_path, exist_ok=True)

        # Eliminar archivos que comienzan con "presupuesto"
        for archiv in os.listdir(folder_path):
            archivo_path = os.path.join(folder_path, archiv)
            if os.path.isfile(archivo_path) and (archiv.startswith("fpresupuesto_firmado_") or archiv.startswith("presupuesto_")):
                servicioDocumento.eliminar_documento(archiv)
                os.remove(archivo_path)

        timestamp = datetime.now().strftime("%Y%m%d")
        filename = os.path.join(folder_path, f"fpresupuesto_firmado_{timestamp}.pdf")

        doc_data = {
            'nombre_documento': f"fpresupuesto_firmado_{timestamp}.pdf",
            'estado_id': 6,
            'legajo_id': id_legajo,
            'tipo_id': 2
        }
        
        archivo.save(os.path.join(folder_path, filename))
        servicioDocumento.crear_documento(doc_data)
        servicioPresupuesto.generar_documento_de_legajo(id_legajo)
        return jsonify({"message": "Presupuesto subido con éxito"}), 200
    except ValidationError as err:
        print(err.messages)  # Imprime los mensajes de error de validación
        return jsonify({"message": f"Error en la validación de los datos: {err.messages}"}), 400
    except Exception as e:
        print(e)  # Imprime el error para depuración
        return jsonify({"message": "Ha ocurrido un error inesperado"}), 500