from models.base import db
from models.documentos.documento import Documento
import os
UPLOAD_FOLDER = os.path.abspath("documentos")
def buscar_documentacion_por_legajo(id_legajo):
    documentacion = Documento.query.filter_by(legajo_id=id_legajo, estado_id=8).first()
    return documentacion

def eliminar_documentacion_anterior(id_legajo):
    documentacion = Documento.query.filter_by(legajo_id=id_legajo, estado_id=8).first()
    if documentacion:
        file_path = os.path.join(UPLOAD_FOLDER, 'informes', str(id_legajo), documentacion.nombre_documento)
        if os.path.exists(file_path):
            os.remove(file_path)

        db.session.delete(documentacion)
        db.session.commit()
    return documentacion

def buscar_informe_por_legajo(id_legajo):
    informe = Documento.query.filter_by(legajo_id=id_legajo, tipo_documento_id=4).filter(Documento.estado_id != 8).first()
    return informe

def buscar_informe_firmado_JA_por_legajo(id_legajo):
    informe = Documento.query.filter_by(legajo_id=id_legajo, tipo_documento_id=4, estado_id=7).first()
    return informe

def eliminar_informe_anterior(id_legajo):
    informe = Documento.query.filter_by(legajo_id=id_legajo, tipo_documento_id=4).filter(Documento.estado_id != 8).first()
    if informe:
        file_path = os.path.join(UPLOAD_FOLDER, 'informes', str(id_legajo), informe.nombre_documento)
        if os.path.exists(file_path):
            os.remove(file_path)

        db.session.delete(informe)
        db.session.commit()
    return informe
    # Eliminar el archivo físico