from servicios.backend.src.core.services import servicioInterarea
from servicios.backend.src.core.services import servicioInterareaArchivos
from flask import Blueprint, jsonify, request, send_file
from servicios.backend.src.web.schemas.interarea import interareaSchema, interareasSchema
from datetime import datetime
import io

bp = Blueprint("interarea", __name__, url_prefix="/interareas")

@bp.get("/")
def listar_interareas():
    interareas = servicioInterarea.listar_interareas()
    data = interareasSchema.dump(interareas)
    print("data:", data)
    return jsonify(data), 200

@bp.get("/<int:id>")
def obtener_interarea(id):
    interarea = servicioInterarea.obtener_interarea(id)
    data = interareaSchema.dump(interarea)
    return jsonify(data), 200

@bp.post("/crear")
def crear_interarea():
    try:
        
        tipo = request.json.get("tipo")
        archivo = servicioInterareaArchivos.generar_solicitud(tipo)

        dataInterarea = {
            "nombre_archivo": archivo,
            "investigacion": request.json.get("investigacion"),
            "nro_investigacion": request.json.get("nro_Investigacion"),
            "legajo_id": request.json.get("legajo"),
            "area_id": request.json.get("area"),
            "muestra_id": request.json.get("muestra"),
        }

        servicioInterarea.crear_interarea(dataInterarea)
            
        return jsonify({"path": archivo}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500
    
@bp.get("/descargar/<path:file_name>")
def descargar_interarea(file_name):
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
def cargar_archivo_completo(id):
    try:
        file = request.files["archivo"]
        servicioInterareaArchivos.subir_archivo_completo(file, id)
        servicioInterarea.cargar_solicitud_completa(id)
        return jsonify({"message": f"Archivo guardado exitosamente en {id}"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500


@bp.post("/cargar_archivo_firmado/<int:id>")
def cargar_archivo_firmado(id):
    try:
        file = request.files["archivo"]
        newFileName = servicioInterareaArchivos.subir_archivo_firmado(file, id)
        servicioInterarea.cargar_solicitud_firmada(id, newFileName)
        return jsonify({"message": f"Archivo guardado exitosamente"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

@bp.post("/guardar_resultado/<int:id>")
def guardar_resultado(id):
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