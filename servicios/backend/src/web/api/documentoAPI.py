from flask_jwt_extended import jwt_required
from models.base import db
from models.legajos import find_legajo_by_id  
from models.documentos import (
    listar_tipos_documentos,
    get_tipo_documento,
    create_documento,
    find_documento,
    find_documento_by_id,
    list_documentos_by_tipo, 
    list_documentos_adicionales_by_legajo
)
from models.documentos import find_estado_by_nombre, listar_documentos
from models.documentos import create_estado
from ..schemas.documento import (
    documentos_schema,
    documento_schema,
    pagination_documento_schema,
)
from ..schemas.tipoDocumento import tipos_documentos_schema, tipo_documento_schema
from servicios.backend.src.web.helpers.auth import check_permission
from flask import Blueprint, abort, request, jsonify, send_file, send_from_directory
from flask import current_app as app
from flask_jwt_extended import jwt_required
from datetime import datetime
from pathlib import Path
import os


bp = Blueprint("documentos", __name__, url_prefix="/api/documentos")


@bp.get("/tipos_documentos")
def list_tipos_documentos():
    data = tipos_documentos_schema.dump(listar_tipos_documentos())
    return jsonify(data), 200


@bp.get("/")
@jwt_required()
def get_documentos():
    if not check_permission("listar_documentos"):
        return jsonify({"message": "No tiene permiso para acceder a este recurso"}), 403
    params = request.args
    page = params.get("page", 1, int)
    per_page = params.get("per_page", 10, int)
    tipo_documento = params.get("tipo_documento", "")
    empresa = params.get("empresa", "")
    fecha = params.get("fecha", "")
    area = params.get("area", "")
    ensayo = params.get("ensayo", "")
    pagination = listar_documentos(
        page=page,
        per_page=per_page,
        tipo_documento=tipo_documento,
        empresa=empresa,
        fecha=fecha,
        area=area,
        ensayo=ensayo,
    )
    data = pagination_documento_schema.dump(pagination)
    return jsonify(data), 200


@bp.post("/upload")
@jwt_required()
def upload():
    if not check_permission("subir_documento"):
        return jsonify({"message": "No tiene permiso para acceder a este recurso"}), 403
    file = request.files["file"]
    tipo = request.form["tipo"]
    legajo_id = request.form["legajo_id"]
    nro_factura = request.form["nro_factura"]

    if file.filename == "" or not file.filename.endswith(".pdf"):
        return jsonify({"error": "Por favor, selecciona un archivo PDF válido"}), 400
    td = get_tipo_documento(tipo)
    if td is None:
        return jsonify({"error": "El tipo de documento no existe"}), 400

    current_file = Path(__file__).resolve()  # Ruta absoluta del archivo actual
    project_root = current_file.parents[5]
    DOCUMENTS_DIR = project_root / "documentos"

    documentos_path = DOCUMENTS_DIR / td.nombre
    documentos_path.mkdir(parents=True, exist_ok=True)

    try:
        file_path = documentos_path / file.filename
        data = {
            "legajo_id": legajo_id,
            "tipo_documento_id": td.id,
            "nombre_documento": None,
        }
        old_file = find_documento(data)
        if old_file:
            old_documento_path = documentos_path / old_file.nombre_documento
            if old_documento_path.exists():
                old_documento_path.unlink()
                file.save(str(file_path))
                old_file.nombre_documento = file.filename
                db.session.commit()
                return (
                    jsonify(
                        {"message": f"Archivo guardado exitosamente en {file_path}"}
                    ),
                    200,
                )
            else:
                return (
                    jsonify(
                        {
                            "error": f"No se encontro el archivo {file.filename}, {old_documento_path}"
                        }
                    ),
                    404,
                )
        else:
            counter = 1
            while file_path.exists():
                file.filename = (
                    f"{Path(file.filename).stem}({counter}){Path(file.filename).suffix}"
                )
                file_path = documentos_path / file.filename
                counter += 1

            data = {
                "nombre_documento": file.filename,
                "fecha_creacion": datetime.now(),
                "estado_id": 1,
                "legajo_id": legajo_id,
                "tipo_documento_id": td.id,
            }
            if not create_documento(data):
                return jsonify({"error": "No se pudo crear el documento"}), 400

            file.save(str(file_path))
            print(nro_factura)
            if nro_factura:
                legajo = find_legajo_by_id(legajo_id)
                if legajo is None:
                    return jsonify({"error": "No se encontro el legajo"}), 404
                legajo.nro_factura = nro_factura
                db.session.commit()
            return (
                jsonify({"message": f"Archivo guardado exitosamente en {file_path}"}),
                200,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.post("/download")
def download():
    data = request.get_json()
    archivo = find_documento(data["params"])
    if archivo is None:
        return jsonify({"error": "No se encontro el archivo"}), 404
    tipo = archivo.tipo_documento.nombre
    filename = archivo.nombre_documento

    # Ruta base de los documentos
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[5]
    documentos_path = project_root / "documentos" / tipo

    # Ruta completa del archivo
    file_path = documentos_path / filename

    # Verificar que el archivo exista
    if not file_path.exists():
        return jsonify({"error": "El archivo no existe"}), 404

    # Enviar el archivo al cliente
    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,  # Nombre que se verá al descargar
    )


@bp.get("/view/<string:filename>")
@jwt_required()
def view_file(filename):
    if not check_permission("ver documentacion"):
        return jsonify({"message": "No tiene permiso para acceder a este recurso"}), 403
    tipo = request.args.get("tipo")  # Recibir el tipo de documento como parámetro
    if not tipo:
        return jsonify({"error": "El tipo de documento es obligatorio"}), 400

    # Ruta base de los documentos
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[5]
    
    documentos_path = project_root / "documentos" / tipo

    # Ruta completa del archivo
    file_path = documentos_path / filename

    # Verificar que el archivo exista
    if not file_path.exists():
        return jsonify({"error": "El archivo no existe"}), 404

    # Enviar el archivo al navegador
    return send_file(
        file_path,
        mimetype=(
            "application/pdf" if filename.endswith(".pdf") else None
        ),  # Cambia el MIME según el tipo de archivo
    )


@bp.get("/<int:id>")
def get_documento(id):
    data = documento_schema.dump(find_documento_by_id(id))
    if data is None:
        return jsonify({"error": "No se encontro el documento"}), 404
    return jsonify(data), 200

@bp.get("/list/<int:tipo>")
def get_documentos_by_tipo(tipo):
    print("entra")
    data = documentos_schema.dump(list_documentos_by_tipo(tipo))
    return jsonify(data), 200

@bp.get("/adicionales/<int:id>")
@jwt_required()
def get_documentos_adicionales(id):
    data = documentos_schema.dump(list_documentos_adicionales_by_legajo(id))
    return jsonify(data), 200

@bp.get("/view_adicional/<int:id>")
@jwt_required()
def view_adicional(id):
    UPLOAD_FOLDER = os.path.abspath("documentos")
    documento = find_documento_by_id(id)
    directory = os.path.normpath(os.path.join(UPLOAD_FOLDER, "adicional"))
    filename = documento.nombre_documento
    file_path = os.path.join(directory, filename)
    if not os.path.exists(file_path):
        print("No existe")
        abort(404, description="El documento no existe, prueba generar uno primero")
    return send_from_directory(directory, filename)