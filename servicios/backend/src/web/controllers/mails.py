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

@bp.post("/subir_mail/<int:id_legajo>")
def cargar_mail(id_legajo):
    if 'archivo' not in request.files:
        return jsonify({"error": "Debes selecionar al menos una imagen"}), 400

    files = request.files.getlist('archivo')
    if not files or all(file.filename == '' for file in files):
        return jsonify({"error": "Por favor seleccione al menos un archivo"}), 400

    for file in files:
        if file and servicioMail.validar_tipo(file.filename):
            if(servicioMail.validar_nombre(file.filename, id_legajo) == False):
                return jsonify({"error": "Ya existe un archivo con ese nombre para el legajo"}), 400
            filename = secure_filename(file.filename)
            folder_path = os.path.join(UPLOAD_FOLDER, "mails", str(id_legajo))
            os.makedirs(folder_path, exist_ok=True)
            file.save(os.path.join(folder_path, filename))
            data = {
                'nombre_archivo': filename,
                'legajo_id': id_legajo
            }
            servicioMail.crear_mail(data, id_legajo)
        else:
            return jsonify({"error": "El tipo del archivo debe ser 'png', 'jpg' o 'jpeg' "}), 400

    return jsonify({"message": "Mails cargados correctamente"}), 200

@bp.post("/eliminar_mail/<int:id_mail>")
def eliminar_mail(id_mail):
    mail = servicioMail.eliminar_mail(id_mail)
    folder_path = os.path.join(UPLOAD_FOLDER, "mails", str(mail.legajo_id))
    file_path = os.path.join(folder_path, mail.nombre_archivo)
    if os.path.exists(file_path):
        os.remove(file_path)
    return jsonify({"message": "Mail eliminado correctamente"}), 200