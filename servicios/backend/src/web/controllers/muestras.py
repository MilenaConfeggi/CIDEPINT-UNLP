from servicios.backend.src.core.services import servicioMuestras
from flask import Blueprint, jsonify, abort, send_from_directory
from servicios.backend.src.core.services import servicioMuestras
from servicios.backend.src.web.schemas.muestras import muestrasSchema
import os

UPLOAD_FOLDER = os.path.abspath("documentos")

bp = Blueprint('muestras', __name__, url_prefix='/muestras')

@bp.get("/<int:id_legajo>")
def listar_muestras_identificadas(id_legajo):
    mails = servicioMuestras.listar_muestras(id_legajo)
    data = muestrasSchema.dump(mails, many=True)
    return jsonify(data), 200

