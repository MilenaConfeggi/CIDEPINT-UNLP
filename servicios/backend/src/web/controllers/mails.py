from marshmallow import ValidationError
from servicios.backend.src.core.services import servicioMail
from flask import Blueprint, jsonify, request
from servicios.backend.src.web.schemas.mails import mailsSchema, mailSchema
from servicios.backend.src.core.config import Config
from werkzeug.utils import secure_filename
import os

# Define allowed file extensions

UPLOAD_FOLDER = "documentos/"

bp = Blueprint('mails', __name__, url_prefix='/mails')

@bp.get("/<int:id_legajo>")
def listar_mails(id_legajo):
    mails = servicioMail.listar_mails(id_legajo)
    data = mailsSchema.dump(mails, many=True)

    return jsonify(data), 200

@bp.post("/subir_mail/<int:id>")
def cargar_mail(id):
    if 'archivo' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['archivo']
    if file.filename == '':
        return jsonify({"error": "Por favor seleccione un archivo"}), 400

    if file and servicioMail.validar_tipo(file.filename):
        filename = secure_filename(file.filename)
        folder_path = os.path.join(UPLOAD_FOLDER, "mails", str(id))
        os.makedirs(folder_path, exist_ok=True)
        file.save(os.path.join(folder_path, filename))
        data = {
            'nombre_archivo': filename,
            'legajo_id': id
        }
        servicioMail.crear_mail(data, id)
        return jsonify({"message": "Mail cargado correctamente"}), 200
    else:
        return jsonify({"error": "El tipo del archivo debe ser 'png', 'jpg' o 'jpeg' "}), 400