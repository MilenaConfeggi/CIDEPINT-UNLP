from flask import Blueprint, request, jsonify
from flask import current_app as app
from models.legajos import (
    list_legajos,
    find_legajo_by_id,
    create_legajo,
    list_legajos_all,
)
from models.documentos import find_estado_by_nombre
from models.clientes import create_cliente
from ..schemas.legajos import legajos_schema, legajo_schema, pagination_legajos_schema
from models.base import db

bp = Blueprint("legajos", __name__, url_prefix="/api/legajos")


@bp.get("/")
def listar_legajos():
    params = request.args
    empresa = params.get("empresa", "")
    fecha = params.get("fecha", "")
    area = params.get("area", "")
    ensayo = params.get("ensayo", "")
    page = params.get("page", 1, int)
    per_page = params.get("per_page", 10, int)
    pagination = list_legajos(
        page=page,
        per_page=per_page,
        empresa=empresa,
        fecha=fecha,
        area=area,
        ensayo=ensayo,
    )
    result = pagination_legajos_schema.dump(pagination)
    return jsonify(result), 200


@bp.get("/<string:id>")
def get_legajo(id):
    data = legajo_schema.dump(find_legajo_by_id(id))
    if data is None:
        return jsonify({"error": "No se encontro el legajo"}), 404
    return jsonify(data), 200


@bp.post("/add")
def add_legajo():
    data = request.get_json()
    legajo = create_legajo(data.get("legajo"))
    if legajo is None:
        return jsonify({"error": "No se pudo crear el legajo"}), 400
    cliente = create_cliente(data.get("cliente"), legajo.id)
    if cliente is None:
        return jsonify({"error": "No se pudo crear el cliente"}), 400
    return jsonify({"message": "Legajo creado"}), 201


@bp.post("/cancel/<int:id>")
def cancel_legajo(id):
    motivo = request.get_json().get("motivo")
    legajo = find_legajo_by_id(id)
    if legajo is None:
        return jsonify({"error": "No se encontro el legajo"}), 404
    legajo.estado = find_estado_by_nombre("Cancelado")
    legajo.motivo_cancelacion = motivo
    db.session.commit()
    return jsonify({"message": "Legajo cancelado"}), 200


@bp.get("/all")
def listado_completo():
    legajos = list_legajos_all()
    data = legajos_schema.dump(legajos)
    return jsonify(data), 200
