from flask import Blueprint, jsonify, request
from models.legajos import cant_legajos_estado
from models.resultados_encuestas import cant_conformidad
from servicios.backend.src.core.services import servicioPresupuesto
from servicios.backend.src.web.schemas.estadistica import estadisticas_schema, estadisticasEnsayo_schema

bp = Blueprint("estadisticas", __name__, url_prefix="/estadisticas")

@bp.get("/")
def obtener_estadisticas_conformidad_legajos():

    legajos_data = [
        {"estado": "Informados", "cantidad": cant_legajos_estado(1)},
        {"estado": "En curso", "cantidad": cant_legajos_estado(2)},
        {"estado": "Terminados", "cantidad": cant_legajos_estado(3)},
        {"estado": "Cancelados", "cantidad": cant_legajos_estado(4)},
    ]

    conformidad = [
        {"categoria": "1", "cantidad": cant_conformidad(1)},
        {"categoria": "2", "cantidad": cant_conformidad(2)},
        {"categoria": "3", "cantidad": cant_conformidad(3)},
        {"categoria": "4", "cantidad": cant_conformidad(4)},
        {"categoria": "5", "cantidad": cant_conformidad(5)},
    ]
    
    estadisticas = {
        "legajos": legajos_data,
        "conformidad": conformidad,
    }

    estadisticas_serializadas = estadisticas_schema.dump(estadisticas)

    return jsonify(estadisticas_serializadas), 200

@bp.post("/ensayos")
def obtener_estadisticas_ensayos():
    
    fecha_desde = request.form.get('startDate')
    fecha_hasta = request.form.get('endDate')

    ensayos = servicioPresupuesto.ensayos_mas_solicitados(fecha_desde, fecha_hasta)
    ensayos_serializados = estadisticasEnsayo_schema.dump(ensayos)

    return jsonify(ensayos_serializados), 200