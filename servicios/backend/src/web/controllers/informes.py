from marshmallow import ValidationError
from servicios.backend.src.core.services import servicioDocumento, servicioInforme
from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

bp = Blueprint("informes", __name__, url_prefix="/informes")
UPLOAD_FOLDER = os.path.abspath("documentos")

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.post("/cargar_documentacion/<int:id_legajo>")
def cargar_documentacion(id_legajo):
    if(servicioInforme.buscar_documentacion_por_legajo(id_legajo)):
        return jsonify({"error": "Ya existe documentación para este legajo"}), 400
    
    if 'archivo' not in request.files:
        return jsonify({"error": "Debes seleccionar un archivo"}), 400

    archivo = request.files['archivo']

    if not archivo or archivo.filename == '':
        return jsonify({"error": "Por favor seleccione un archivo"}), 400

    if not allowed_file(archivo.filename):
        return jsonify({"error": "Tipo de archivo no permitido. Solo se permiten archivos PDF o del paquete Office."}), 400

    try:
        filename = secure_filename(archivo.filename).replace(" ", "_")  # Reemplazar espacios con guion bajo
        doc_data = {
            'nombre_documento': filename,
            'estado_id': 1,
            'legajo_id': id_legajo,
            'tipo_id': 1
        }

        # Guardar el archivo en el servidor
        folder_path = os.path.join(UPLOAD_FOLDER, "informes", str(id_legajo))
        os.makedirs(folder_path, exist_ok=True)
        archivo.save(os.path.join(folder_path, filename))
        servicioDocumento.crear_documento(doc_data)
        return jsonify({"message": "Documentación subida con éxito"}), 200
    except ValidationError as err:
        print(err.messages)  # Imprime los mensajes de error de validación
        return jsonify({"message": f"Error en la validación de los datos: {err.messages}"}), 400
    except Exception as e:
        print(e)  # Imprime el error para depuración
        return jsonify({"message": "Ha ocurrido un error inesperado"}), 500