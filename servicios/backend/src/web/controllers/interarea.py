from servicios.backend.src.core.services import servicioInterarea
from servicios.backend.src.core.services import servicioInterareaArchivos
from flask import Blueprint, jsonify, request, send_file
from servicios.backend.src.web.schemas.interarea import interareaSchema, interareasSchema
from datetime import datetime
import io
from servicios.backend.src.web.helpers.auth import is_authenticated, check_permission
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("interarea", __name__, url_prefix="/interareas")

@bp.get("/")
@jwt_required()
def listar_interareas():#No se, por las dudas pongo a todos
    if not check_permission("listar_interareas"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    interareas = servicioInterarea.listar_interareas()
    data = interareasSchema.dump(interareas)
    return jsonify(data), 200

@bp.get("/<int:id>")
@jwt_required()
def obtener_interarea(id):#No se por las dudas pongo a todos
    if not check_permission("obtener_interarea"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    interarea = servicioInterarea.obtener_interarea(id)
    data = interareaSchema.dump(interarea)
    return jsonify(data), 200

@bp.post("/crear")
@jwt_required()
def crear_interarea():#Jefes de área
    if not check_permission("crear_intearea"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    try:
        tipo = request.json.get("tipo")
        archivo = servicioInterareaArchivos.generar_solicitud(tipo)
        dataInterarea = {
            "nombre_archivo": archivo,
            "investigacion": request.json.get("investigacion"),
            "nro_investigacion": request.json.get("lineaInvestigacion"),
            "legajo_id": None if request.json.get("legajo") == "" else request.json.get("legajo"),
            "area_solicitante_id": request.json.get("area_solicitante_id"),
            "area_receptora_id": request.json.get("area_receptora_id"),
            "muestra_id": None if request.json.get("muestra") == "" else request.json.get("muestra"),
            "muestra_investigacion": request.json.get("muestra_investigacion")
        }
        servicioInterarea.crear_interarea(dataInterarea)
            
        return jsonify({"path": archivo}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500
    
@bp.get("/descargar/<path:file_name>")
@jwt_required()
def descargar_interarea(file_name):#Todos
    if not check_permission("descargar_intearea"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    try:
        file_stream = servicioInterareaArchivos.descargar_solicitud(file_name)
        if file_stream is not None:
            return send_file(
                file_stream,
                as_attachment=True,
                download_name=file_name,  
                mimetype="application/pdf"  
            )
        return jsonify({"error": "No se pudo descargar el archivo"}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

@bp.post("/cargar_archivo_completo/<int:id>")
@jwt_required()
def cargar_archivo_completo(id):#Trabajador y Jefe de Área
    if not check_permission("cargar_archivo_completo"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    try:
        file = request.files["archivo"]
        servicioInterareaArchivos.subir_archivo_completo(file, id)
        servicioInterarea.cargar_solicitud_completa(id)
        return jsonify({"message": f"Archivo guardado exitosamente en {id}"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500


@bp.post("/cargar_archivo_firmado/<int:id>")
@jwt_required()
def cargar_archivo_firmado(id):#Secretaria y Director
    if not check_permission("cargar_archivo_firmado"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    try:
        file = request.files["archivo"]
        newFileName = servicioInterareaArchivos.subir_archivo_firmado(file, id)
        servicioInterarea.cargar_solicitud_firmada(id, newFileName)
        return jsonify({"message": f"Archivo guardado exitosamente"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

@bp.post("/guardar_resultado/<int:id>")
@jwt_required()
def guardar_resultado(id):#Jefes de áreas
    if not check_permission("guardar_resultado"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    try:
        data = {
            "resultados": request.json.get("resultado"),
            "estadoInterarea_id": 3,
        }
        servicioInterarea.guardar_resultado(id, data)
        return jsonify({"message": "Resultado guardado exitosamente"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500
    
@bp.post("/guardar_resultado_documentos/<int:id>")
@jwt_required()
def guardar_resultado_documentos(id):
    if not check_permission("guardar_resultado"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    try:
        documentos = request.files.getlist("documentos")  
        servicioInterareaArchivos.guardar_documentos_resultado(id, documentos)
        return jsonify({"message": "Resultado guardado exitosamente"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500
    
@bp.get("/descargar_resultado_documentos/<int:id>")
@jwt_required()
def descargar_resultado_documentos(id):
    if not check_permission("descargar_resultado_interarea"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    try:
        print("Descargando archivos...")
        archivos = servicioInterareaArchivos.descargar_resultado(id)
        return send_file(
            archivos,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"resultados_interarea-{id}.zip"
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500
