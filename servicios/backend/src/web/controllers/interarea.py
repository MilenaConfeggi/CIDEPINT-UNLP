from servicios.backend.src.core.services import servicioInterarea
from flask import Blueprint, jsonify, request
from servicios.backend.src.web.schemas.interarea import interareaSchema, interareasSchema

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
    data = request.get_json()
    interarea = servicioInterarea.crear_interarea(data)
    data = interareaSchema.dump(interarea)
    return jsonify(data), 201   