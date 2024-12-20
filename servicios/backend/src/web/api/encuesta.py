from flask import Blueprint, request, jsonify
from flask import current_app as app
from models.base import db
from models.resultados_encuestas.resultado_encuesta import ResultadoEncuesta
from models.resultados_encuestas import create_resultado_encuesta, find_resultado_encuesta_by_unique_key


bp = Blueprint('encuestas', __name__, url_prefix='/api/encuestas')

@bp.get('/')
def get_encuesta():
    id = request.args.get('id')
    encuesta = find_resultado_encuesta_by_unique_key(id)
    if encuesta is None:
        return jsonify({"error": "No se encontro la encuesta"}), 404
    return jsonify({"completed": encuesta.completado}), 200

@bp.get('/add')
def add_encuesta():
    params = request.args
    unique_key = params.get('unique_key')
    print(unique_key)
    encuesta = create_resultado_encuesta(unique_key)
    if encuesta is None:
        return jsonify({"error": "No se pudo crear la encuesta"}), 400
    db.session.add(encuesta)
    db.session.commit()
    return jsonify({"message": "Encuesta creada"}), 200

@bp.post('/complete')
def complete_encuesta():
    params = request.args
    data = request.get_json()
    client_data = data.get('clientData')
    temas = data.get('temas')
    print(data)
    unique_key = params.get('id')
    print(unique_key)
    encuesta = find_resultado_encuesta_by_unique_key(unique_key)
    if encuesta is None:
        return jsonify({"error": "No se pudo completar la encuesta"}), 400
    encuesta.completado = True
    encuesta.como_conocio_cidepint = data.get('como_conocio_cidepint')
    encuesta.precio_del_servicio = temas.get('precio_servicio')
    encuesta.calificacion_general = data.get('calificacion_general')
    encuesta.atencion_adminstracion = temas.get('atencion_admin')
    encuesta.servicio_ofercido_laboratorio = temas.get('servicio_ofrecido')
    encuesta.resulatdo_del_ensayo = temas.get('resultado_ensayo')
    encuesta.asesoramiento_brindado = temas.get('asesoramiento')
    encuesta.cumplimiento_de_los_plazos = temas.get('cumplimiento')
    encuesta.sistema_de_pago = temas.get('sistema_de_pago')
    encuesta.otros = data.get('otros')
    db.session.commit()
    return jsonify({"message": "Encuesta completada"}), 200