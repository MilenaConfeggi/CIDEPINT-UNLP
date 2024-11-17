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
    data = request.get_json()
    muestras = []
    for elem in data:
        elem['fecha_ingreso'] = elem.pop('fechaIngreso')
        elem['iden_cliente'] = elem.pop('idenCliente')
        muestra = muestraSchema.load(elem)
        muestras.append(muestra)
        #valido que no haya muestras cargadas previamente con la misma identificacion
        if(servicioMuestras.validar_identificacion_cliente(muestra, id_legajo) == False):
            return jsonify({"message": f"Ya se ingresó la identificación {elem['iden_cliente']} para este legajo"}), 400
        #valido que entre las que se cargar al mismo tiempo no tengan la misma identificacion
        if(servicioMuestras.validar_entre_cargadas(muestras, muestra) == False):
            return jsonify({"message": f"La identificación {elem['iden_cliente']} está siendo ingresada más de una vez en este lote. Modificalo y vuelve a intentar"}), 400
    for muestra in muestras:
        muestra = servicioMuestras.crear_muestra(muestra, id_legajo)

    return jsonify({"message": "Muestras cargadas correctamente"}), 200
