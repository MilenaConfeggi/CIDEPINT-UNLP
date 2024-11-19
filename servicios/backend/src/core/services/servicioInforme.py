from models.base import db
from models.documentos.documento import Documento

def buscar_documentacion_por_legajo(id_legajo):
    documentacion = Documento.query.filter_by(legajo_id=id_legajo, estado_id=1).all()
    if documentacion:
        return documentacion
    return False