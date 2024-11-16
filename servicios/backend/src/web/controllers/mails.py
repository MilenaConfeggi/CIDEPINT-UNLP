from servicios.backend.src.core.config import Config
from werkzeug.utils import secure_filename, safe_join
import os
from flask import send_from_directory, jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioMail
from servicios.backend.src.web.schemas.mails import mailsSchema

# Define allowed file extensions

UPLOAD_FOLDER = os.path.abspath("documentos")

bp = Blueprint('mails', __name__, url_prefix='/mails')

@bp.get("/<int:id_legajo>")
def listar_mails(id_legajo):
    mails = servicioMail.listar_mails(id_legajo)
    data = mailsSchema.dump(mails, many=True)
    return jsonify(data), 200

@bp.get("/imagenes/<int:id_legajo>/<filename>")
def obtener_imagen(id_legajo, filename):
    folder_path = os.path.normpath(os.path.join(UPLOAD_FOLDER, "mails", str(id_legajo)))
    file_path = os.path.normpath(os.path.join(folder_path, filename))
    print(f"Folder path: {folder_path}")
    print(f"File path: {file_path}")
    if not os.path.exists(file_path):
        print("File not found")
        abort(404, description="Resource not found")
    print("File found, sending from directory")
    return send_from_directory(folder_path, filename)

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