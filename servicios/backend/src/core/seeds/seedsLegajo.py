from datetime import datetime
from models.legajos.legajo import Legajo
from models.base import db

def seeds_legajos():

    legajos_data = [
        {
            'fecha_entrada': datetime(2024, 1, 1),
            'nro_legajo': 'LEG1',
            'es_juridico': True,
            'necesita_facturacion': True,
            'motivo_cancelacion': None,
            'cliente_id': 1
        },
        {
            'fecha_entrada': datetime(2024, 2, 1),
            'nro_legajo': 'LEG2',
            'es_juridico': False,
            'necesita_facturacion': False,
            'motivo_cancelacion': None,
            'cliente_id': 2
        },
        {
            'fecha_entrada': datetime(2024, 3, 1),
            'nro_legajo': 'LEG3',
            'es_juridico': True,
            'necesita_facturacion': True,
            'motivo_cancelacion': None,
            'cliente_id': 3
        }
    ]

    for data in legajos_data:
        db.session.add(Legajo(**data))
        db.session.commit()
