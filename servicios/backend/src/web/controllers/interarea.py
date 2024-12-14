from servicios.backend.src.core.services import servicioInterarea
from servicios.backend.src.core.services import servicioInterareaPDF
from flask import Blueprint, jsonify, request
from servicios.backend.src.web.schemas.interarea import interareaSchema, interareasSchema
from datetime import datetime

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
            "nombre_solicitud_no_firmada": archivo,
            "investigacion": request.json.get("investigacion"),
            "legajo_id": request.json.get("legajo"),
            "area_id": request.json.get("area"),
            "muestra_id": request.json.get("muestra"),
        }

        servicioInterarea.crear_interarea(dataInterarea)
            
        return jsonify({"message": "interarea creada", "path": archivo}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500