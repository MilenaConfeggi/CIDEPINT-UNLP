from models.base import db
from models.documentos import listar_tipos_documentos, get_tipo_documento, create_documento, find_documento
from models.documentos import find_estado_by_nombre
from models.documentos import create_estado
from flask import Blueprint, request, jsonify, send_file
from flask import current_app as app
from datetime import datetime
from pathlib import Path
import os


bp = Blueprint('documentos', __name__, url_prefix='/api/documentos')

@bp.post('/upload')
def upload():
    file = request.files['file']
    tipo = request.form['tipo']
    legajo_id = request.form['legajo_id']
    
    if file.filename == '' or not file.filename.endswith('.pdf'):
        return jsonify({"error": "Por favor, selecciona un archivo PDF válido"}), 400
    td = get_tipo_documento(tipo)
    if td is None:
        return jsonify({"error": "El tipo de documento no existe"}), 400
    
    current_file = Path(__file__).resolve()  # Ruta absoluta del archivo actual
    project_root = current_file.parents[5]  
    DOCUMENTS_DIR = project_root / 'documentos'
    
    documentos_path = DOCUMENTS_DIR / td.nombre
    documentos_path.mkdir(parents=True, exist_ok=True)

    try:        
        data = {
            'nombre_documento': file.filename,
            'fecha_creacion': datetime.now(),
            'estado_id': 1,
            'legajo_id': legajo_id,
            'tipo_documento_id': tipo,
        }
        if not create_documento(data):
            return jsonify({"error": "No se pudo crear el documento"}), 400
        
        file_path = documentos_path / file.filename
        counter = 1
        while file_path.exists():
            new_filename = f"{file.stem}({counter}){file.suffix}"  
            file_path = documentos_path / new_filename
            counter += 1
        
        file.save(str(file_path))
        return jsonify({"message": f"Archivo guardado exitosamente en {file_path}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bp.post('/download')
def download():
    data = request.get_json()
    archivo = find_documento(data['params'])
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
        download_name=filename  # Nombre que se verá al descargar
    )