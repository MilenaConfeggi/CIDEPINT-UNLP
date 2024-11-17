from servicios.backend.src.core.services import servicioMuestras
from flask import Blueprint, jsonify, abort, request, send_from_directory
from servicios.backend.src.web.schemas.muestras import muestrasSchema, muestraSchema
import os
from marshmallow import ValidationError

UPLOAD_FOLDER = os.path.abspath("documentos")

bp = Blueprint('muestras', __name__, url_prefix='/muestras')

@bp.get("/<int:id_legajo>")
def listar_muestras_identificadas(id_legajo):
    mails = servicioMuestras.listar_muestras(id_legajo)
    data = muestrasSchema.dump(mails, many=True)
    return jsonify(data), 200

@bp.post("/subir_muestras/<int:id_legajo>")
def cargar_muestra(id_legajo):
    try:
        data = request.get_json()
        muestras = []
        for elem in data:
            elem['fecha_ingreso'] = elem.pop('fechaIngreso')
            elem['iden_cliente'] = elem.pop('idenCliente')
            try:
                muestra = muestraSchema.load(elem)
            except ValidationError as err:
                return jsonify({"message": f"Error en la fecha para la identificación {elem['iden_cliente']}"}), 400
            muestra = muestraSchema.load(elem)
            #valido que no haya muestras cargadas previamente con la misma identificacion
            if not servicioMuestras.validar_identificacion_cliente(muestra, id_legajo):
                return jsonify({"message": f"Ya se ingresó la identificación {elem['iden_cliente']} para este legajo"}), 400
            #valido que entre las que se cargar al mismo tiempo no tengan la misma identificacion
            if not servicioMuestras.validar_entre_cargadas(muestras, muestra):
                return jsonify({"message": f"La identificación {elem['iden_cliente']} está siendo ingresada más de una vez en este lote. Modificalo y vuelve a intentar"}), 400
            if not servicioMuestras.validar_longitud(muestra):
                return jsonify({"message": "La identificación del cliente no puede superar los 100 caracteres"}), 400
            if not servicioMuestras.validar_fecha(muestra):
                return jsonify({"message": "La fecha de ingreso no puede ser mayor a la fecha actual"}), 400
            muestras.append(muestra)
        for muestra in muestras:
            muestra = servicioMuestras.crear_muestra(muestra, id_legajo)

        return jsonify({"message": "Muestras cargadas correctamente"}), 200
    except ValidationError as e:
        return jsonify({"message": "Ha ocurrido un error inesperado, revise que muestras se han cargado antes de volver a intentarlo"}), 400
    except Exception as e:
        return jsonify({"message": "Ha ocurrido un error inesperado, revise que muestras se han cargado antes de volver a intentarlo"}), 500