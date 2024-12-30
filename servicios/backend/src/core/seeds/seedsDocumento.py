from models.documentos.documento import Documento
from models.documentos.tipo_documento import Tipo_Documento
from models.documentos.estado import Estado
from models.base import db
from datetime import datetime

def seeds_documentos():
    documentos_data = [
        {
            'nombre_documento': 'Documento 2',
            'fecha_creacion': datetime(2024, 1, 1),
            'estado_id': 2,
            'tipo_documento_id': 2,
            'legajo_id': 33
        },
        {
            'nombre_documento': 'Documento 3',
            'fecha_creacion': datetime(2024, 1, 1),
            'estado_id': 3,
            'tipo_documento_id': 3,
            'legajo_id': 33
        },
        {
            'nombre_documento': 'Documento 4',
            'fecha_creacion': datetime(2024, 1, 1),
            'estado_id': 4,
            'tipo_documento_id': 4,
            'legajo_id': 33
        },
        {    'nombre_documento': 'orden_compra',
            'fecha_creacion': datetime(2024, 1, 1),
            'estado_id': 1,
            'tipo_documento_id': 5,
            'legajo_id': 33
        },
    ]
    for data in documentos_data:
        db.session.add(Documento(**data))
    db.session.commit()
def seeds_tipos_documento():

    tipos_documento_data = [
        {
            'nombre': 'Certificado CIDEPINT',
        },
        {
            'nombre': 'Presupuesto CIDEPINT',
        },
        {
            'nombre': 'Presupuesto CONICET',
        },
        {
            'nombre': 'Informe',
        },
        {
            'nombre': 'Orden de compra',
        },
        {
            'nombre': 'Factura',
        },
        {
            'nombre': 'orden_facturacion',
        },
        {
            'nombre': 'adicional',
        },
        {
            'nombre': 'Legajo',
        },
    ]
    for data in tipos_documento_data:
        db.session.add(Tipo_Documento(**data))
    db.session.commit()
