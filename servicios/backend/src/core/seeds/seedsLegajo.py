from datetime import datetime
from models.legajos.legajo import Legajo
from models.clientes.cliente import Cliente
from models.legajos import create_legajo, find_legajo_by_id
from models.clientes import find_cliente_by_mail
from models.base import db

def seeds_legajos():
    
    

    legajos_data = [
        {
            'fecha_entrada': datetime(2024, 1, 1),
            'nro_legajo': 'LEG1',
            'es_juridico': True,
            'necesita_facturacion': True,
            'objetivo': 'Objetivo de legajo',
        },
        {
            'fecha_entrada': datetime(2024, 1, 1),
            'nro_legajo': 'LEG2',
            'es_juridico': True,
            'necesita_facturacion': True,
            'objetivo': 'Objetivo de legajo2',

        },
        {
            'fecha_entrada': datetime(2024, 2, 1),
            'nro_legajo': 'LEG3',
            'es_juridico': False,
            'necesita_facturacion': False,
            'objetivo': 'Objetivo de legajo3',
        },
        {
            'fecha_entrada': datetime(2024, 3, 1),
            'nro_legajo': 'LEG4',
            'es_juridico': True,
            'necesita_facturacion': True,
            'objetivo': 'Objetivo de legajo4',
        }
    ]
    for data in legajos_data:
        create_legajo(data)
    db.session.commit()