from servicios.backend.src.core.services import servicioInterarea
from servicios.backend.src.core.services import servicioInterareaPDF
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
        dataPDF = {
            "tipo": request.json.get("tipo"),
            "identificacion": request.json.get("lineaInvestigacion") if request.json.get("legajo") is None else request.json.get("legajo"),
            "solicitante": request.json.get("solicitante"),
            "fecha": datetime.now().strftime("%d-%m-%Y"),
            "material": request.json.get("material"),
            "cantidad": request.json.get("cantidad"),
        }
        
        archivo = servicioInterareaPDF.generar_pdf(dataPDF)

        dataInterarea = {
            "investigacion": request.json.get("investigacion"),
            "nro_investigacion": request.json.get("nro_Investigacion"),
            "legajo_id": request.json.get("legajo"),
            "area_id": request.json.get("area"),
            "muestra_id": request.json.get("muestra"),
        }

        interarea = servicioInterarea.crear_interarea(dataInterarea)
            
        return jsonify({"path": archivo, "id": interarea.id}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500
    
@bp.get("/descargar/<path:file_name>")
def descargar_interarea(file_name):
    try:
        file_stream = servicioInterareaPDF.descargar_solicitud(file_name)
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

@bp.post("/cargar_archivo_completo/<path:file_name>")
def cargar_archivo_completo(file_name):
    try:
        file = request.files["archivo"]
        file_path = servicioInterareaPDF.subir_archivo_completo(file, file_name)
        id = request.json.get("id")
        servicioInterarea.cargar_solicitud_completa(id, file_name)
        return jsonify({"message": f"Archivo guardado exitosamente en {file_path}"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500


@bp.post("/cargar_archivo_firmado/<path:file_name>")
def cargar_archivo_firmado(file_name):
    try:
        file = request.files["archivo"]
        file_path = servicioInterareaPDF.subir_archivo_firmado(file, file_name)
        id = request.json.get("id")
        servicioInterarea.cargar_solicitud_firmada(id, file_name)
        return jsonify({"message": f"Archivo guardado exitosamente en {file_path}"}), 200
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