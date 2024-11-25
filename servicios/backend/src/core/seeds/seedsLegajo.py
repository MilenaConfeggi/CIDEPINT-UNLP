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
            'motivo_cancelacion': None,
        },
        {
            'fecha_entrada': datetime(2024, 1, 1),
            'nro_legajo': 'LEG1',
            'es_juridico': True,
            'necesita_facturacion': True,
            'motivo_cancelacion': None,

        },
        {
            'fecha_entrada': datetime(2024, 2, 1),
            'nro_legajo': 'LEG2',
            'es_juridico': False,
            'necesita_facturacion': False,
            'motivo_cancelacion': None,
        },
        {
            'fecha_entrada': datetime(2024, 3, 1),
            'nro_legajo': 'LEG3',
            'es_juridico': True,
            'necesita_facturacion': True,
            'motivo_cancelacion': None,
        }
    ]
    cliente_data = {
            'email': 'cliente1@mail.com',
            'cuit': '123456789',
            'telefono': '123456789',
            'celular': '123456789',
            'direccion': 'Calle 1',
            'fecha_nacimiento': datetime(1990, 1, 1),
            'contacto': 'Contacto 1',
            'calle': 'Calle 1',
            'numero': '1',
            'localidad': 'Localidad 1',
            'codigo_postal': '00000',
            'piso': 'Piso 1',
            'depto': 'Depto 1',
            'legajo_id': 1
        }

    for data in legajos_data:
        create_legajo(data)
    
    c = Cliente(**cliente_data)
    db.session.add(c)
    
    cli = find_cliente_by_mail(cliente_data['email'])
    print(cli.legajo.nro_legajo)
    
    leg = find_legajo_by_id("LEG1")
    print(leg.cliente.cuit)
    
    db.session.commit()