from marshmallow import ValidationError
from servicios.backend.src.core.services import servicioDocumento, servicioInforme, servicioUsuario
from flask import Blueprint, abort, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from models.base import db
from models.documentos.documento import Documento
from models.legajos import legajo_informado, legajo_en_curso
from flask_jwt_extended import jwt_required, get_jwt_identity

# Importa check_permission desde el módulo correspondiente
from servicios.backend.src.web.helpers.auth import check_permission

bp = Blueprint("informes", __name__, url_prefix="/informes")
UPLOAD_FOLDER = os.path.abspath("documentos")

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.post("/cargar_documentacion/<int:id_legajo>")
@jwt_required()
def cargar_documentacion(id_legajo):
    if not check_permission("cargar_documentacion"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    if(servicioInforme.buscar_documentacion_por_legajo(id_legajo)):
        mensaje = "Se ha eliminado la documentación anterior e informes en caso de que los hubiera"
    else:
        mensaje = " "
    if 'archivo' not in request.files:
        return jsonify({"error": "Debes seleccionar un archivo"}), 400

    archivo = request.files['archivo']

    if not archivo or archivo.filename == '':
        return jsonify({"error": "Por favor seleccione un archivo"}), 400

    if not allowed_file(archivo.filename):
        return jsonify({"error": "Tipo de archivo no permitido. Solo se permiten archivos PDF o del paquete Office."}), 400

    try:
        filename = secure_filename(archivo.filename).replace(" ", "_")  # Reemplazar espacios con guion bajo
        doc_data = {
            'nombre_documento': filename,
            'estado_id': 8,
            'legajo_id': id_legajo,
            'tipo_id': 4
        }
        # Guardar el archivo en el servidor
        folder_path = os.path.join(UPLOAD_FOLDER, "informes", str(id_legajo))
        os.makedirs(folder_path, exist_ok=True)
        archivo.save(os.path.join(folder_path, filename))
        doc = servicioDocumento.crear_documento(doc_data)
        return jsonify({"message": "Documentación subida con éxito", "info": mensaje}), 200
    except ValidationError as err:
        print(err.messages)  # Imprime los mensajes de error de validación
        return jsonify({"message": f"Error en la validación de los datos: {err.messages}"}), 400
    except Exception as e:
        print(e)  # Imprime el error para depuración
        return jsonify({"message": "Ha ocurrido un error inesperado"}), 500
    
@bp.get("/ver_documento/<int:id_legajo>")
@jwt_required()
def ver_documento(id_legajo):
    folder_path = os.path.normpath(os.path.join(UPLOAD_FOLDER, "informes", str(id_legajo)))
    documentacion = servicioInforme.buscar_documentacion_por_legajo(id_legajo)
    if not documentacion:
        return jsonify({"error": "No hay documentacion para este legajo"}), 404

    filename = documentacion.nombre_documento
    file_path = os.path.normpath(os.path.join(folder_path, filename))
    if not os.path.exists(file_path):
        abort(404, description="Resource not found")
    return send_from_directory(folder_path, filename)

def permitir_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {"pdf"}

@bp.post("/cargar_informe/<int:id_legajo>")
@jwt_required()
def cargar_informe(id_legajo):
    if not check_permission("cargar_informe"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    if 'archivo' not in request.files:
        return jsonify({"error": "Debes seleccionar un archivo"}), 400

    archivo = request.files['archivo']

    if not archivo or archivo.filename == '':
        return jsonify({"error": "Por favor seleccione un archivo"}), 400

    if not permitir_pdf(archivo.filename):
        return jsonify({"error": "Tipo de archivo no permitido. Solo se permiten archivos PDF o del paquete Office."}), 400
    
    try:
        filename = secure_filename(archivo.filename).replace(" ", "_")  # Reemplazar espacios con guion bajo
        user = get_jwt_identity()
        doc_data = {
            'nombre_documento': filename,
            'estado_id': 5,
            'legajo_id': id_legajo,
            'tipo_id': 4
        }

        # Guardar el archivo en el servidor
        folder_path = os.path.join(UPLOAD_FOLDER, "informes", str(id_legajo))
        os.makedirs(folder_path, exist_ok=True)
        archivo.save(os.path.join(folder_path, filename))
        servicioDocumento.crear_documento(doc_data)
        return jsonify({"message": "Informe subido con éxito"}), 200
    except ValidationError as err:
        print(err.messages)  # Imprime los mensajes de error de validación
        return jsonify({"message": f"Error en la validación de los datos: {err.messages}"}), 400
    except Exception as e:
        print(e)  # Imprime el error para depuración
        return jsonify({"message": "Ha ocurrido un error inesperado"}), 500
    
@bp.get("/ver_informe/<int:id_legajo>")
@jwt_required()
def ver_informe(id_legajo):
    folder_path = os.path.normpath(os.path.join(UPLOAD_FOLDER, "informes", str(id_legajo)))
    documentacion = servicioInforme.buscar_informe_por_legajo(id_legajo)
    if not documentacion:
        return jsonify({"error": "No hay informe para este legajo"}), 404

    filename = documentacion.nombre_documento
    file_path = os.path.normpath(os.path.join(folder_path, filename))
    if not os.path.exists(file_path):
        abort(404, description="Resource not found")
    return send_from_directory(folder_path, filename)

@bp.post("/cargar_informe_firmado/<int:id_legajo>")
@jwt_required()
def cargar_informe_firmado(id_legajo):
    if not check_permission("cargar_informe_firmado"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    if 'archivo' not in request.files:
        return jsonify({"error": "Debes seleccionar un archivo"}), 400

    archivo = request.files['archivo']

    if not archivo or archivo.filename == '':
        return jsonify({"error": "Por favor seleccione un archivo"}), 400

    if not permitir_pdf(archivo.filename):
        return jsonify({"error": "Tipo de archivo no permitido. Solo se permiten archivos PDF o del paquete Office."}), 400
    
    if not servicioInforme.buscar_informe_por_legajo(id_legajo):
        return jsonify({"error": "No hay informe para este legajo"}), 404
    
    try:
        filename = secure_filename(archivo.filename).replace(" ", "_")  
        # Eliminar el informe anterior
        #chequeo si quien hizo la peticion es un jefe de area o un director
        user = get_jwt_identity()
        usuario = servicioUsuario.obtener_usuario_por_mail(user)
        if servicioUsuario.es_jefe_de_area(usuario):
            print("es jefe de area")
            doc_data = {
                'nombre_documento': filename,
                'estado_id': 7,
                'legajo_id': id_legajo,
                'tipo_id': 4
            }
        else:
            if servicioUsuario.es_director(usuario):
                if not servicioInforme.buscar_informe_firmado_JA_por_legajo(id_legajo):
                    return jsonify({"error": "No hay informe firmado por el jefe de área"}), 404
                doc_data = {
                    'nombre_documento': filename,
                    'estado_id': 6,
                    'legajo_id': id_legajo,
                    'tipo_id': 4
                }
            else:
                return jsonify({"error": "No tienes permisos para realizar esta acción"}), 403
        # Guardar el archivo en el servidor
        folder_path = os.path.join(UPLOAD_FOLDER, "informes", str(id_legajo))
        os.makedirs(folder_path, exist_ok=True)
        archivo.save(os.path.join(folder_path, filename))
        servicioDocumento.crear_documento(doc_data)
        return jsonify({"message": "Informe subido con éxito"}), 200
    except ValidationError as err:
        print(err.messages)  # Imprime los mensajes de error de validación
        return jsonify({"message": f"Error en la validación de los datos: {err.messages}"}), 400
    except Exception as e:
        print(e)  # Imprime el error para depuración
        return jsonify({"message": "Ha ocurrido un error inesperado"}), 500
    
@bp.get("/ver_todos_informes/<int:id_legajo>")
@jwt_required()
def ver_todos_informes(id_legajo):
    informes = servicioInforme.buscar_todos_informes_por_legajo(id_legajo)
    if not informes:
        # Devolver un objeto con categorías vacías si no hay informes
        return jsonify({
            "DOCUMENTACIONES": [],
            "INFORMES": [],
            "INFORMES_FIRMADOS_JA": [],
            "INFORMES_FIRMADOS_DIRECTOR": []
        }), 200

    # Agrupar los documentos por estado
    agrupados = {
        "DOCUMENTACIONES": [],
        "INFORMES": [],
        "INFORMES_FIRMADOS_JA": [],
        "INFORMES_FIRMADOS_DIRECTOR": []
    }

    for informe in informes:
        if informe.estado_id == 8:
            agrupados["DOCUMENTACIONES"].append({"id": informe.id, "nombre_documento": informe.nombre_documento})
        elif informe.estado_id == 5:
            agrupados["INFORMES"].append({"id": informe.id, "nombre_documento": informe.nombre_documento})
        elif informe.estado_id == 7:
            agrupados["INFORMES_FIRMADOS_JA"].append({"id": informe.id, "nombre_documento": informe.nombre_documento})
        elif informe.estado_id == 6:
            agrupados["INFORMES_FIRMADOS_DIRECTOR"].append({"id": informe.id, "nombre_documento": informe.nombre_documento})

    return jsonify(agrupados), 200

@bp.get("/ver_informe_por_id/<int:id_informe>")
@jwt_required()
def ver_informe_por_id(id_informe):
    informe = servicioInforme.buscar_informe_por_id(id_informe)
    if not informe:
        return jsonify({"error": "No se encontró el informe solicitado"}), 404

    folder_path = os.path.normpath(os.path.join(UPLOAD_FOLDER, "informes", str(informe.legajo_id)))
    file_path = os.path.normpath(os.path.join(folder_path, informe.nombre_documento))
    if not os.path.exists(file_path):
        abort(404, description="El archivo no existe")
    return send_from_directory(folder_path, informe.nombre_documento)

@bp.post("/marcar_informado/<int:id_legajo>")
@jwt_required()
def marcar_informado(id_legajo):
    if not check_permission("cargar_informe"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    try:
        legajo_informado(id_legajo)
        return jsonify({"message": "El legajo ha sido marcado como informado."}), 200
    except Exception as e:
        print(f"Error al marcar el legajo como informado: {e}")
        return jsonify({"error": "Error interno del servidor."}), 500

@bp.get("/eliminar_informe/<int:id_informe>")
@jwt_required()
def eliminar_informe(id_informe):
    if not check_permission("cargar_informe"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    try:
        informe = servicioInforme.buscar_informe_por_id(id_informe)
        if not informe:
            return jsonify({"error": "No se encontró el informe solicitado"}), 404

        folder_path = os.path.normpath(os.path.join(UPLOAD_FOLDER, "informes", str(informe.legajo_id)))
        file_path = os.path.normpath(os.path.join(folder_path, informe.nombre_documento))
        if os.path.exists(file_path):
            os.remove(file_path)
        servicioInforme.eliminar_informe(id_informe)
        return jsonify({"message": "Informe eliminado con éxito"}), 200
    except Exception as e:
        print(f"Error al eliminar el informe: {e}")
        return jsonify({"error": "Error interno del servidor."}), 500