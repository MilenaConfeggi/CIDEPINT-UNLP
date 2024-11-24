from datetime import datetime
from models.clientes.cliente import Cliente
from models.base import db

def seeds_clientes():
    clientes_data = [
        {
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
        },
        {
            'email': 'cliente2@mail.com',
            'cuit': '123456789',
            'telefono': '123456789',
            'celular': '123456789',
            'direccion': 'Calle 2',
            'fecha_nacimiento': datetime(1990, 1, 1),
            'contacto': 'Contacto 2',
            'calle': 'Calle 2',
            'numero': '2',
            'localidad': 'Localidad 2',
            'codigo_postal': '00000',
            'piso': 'Piso 2',
            'depto': 'Depto 2',
            'legajo_id': 2
        },
        {
            'email': 'cliente3@mail.com',
            'cuit': '123456789',
            'telefono': '123456789',
            'celular': '123456789',
            'direccion': 'Calle 3',
            'fecha_nacimiento': datetime(1990, 1, 1),
            'contacto': 'Contacto 3',
            'calle': 'Calle 3',
            'numero': '3',
            'localidad': 'Localidad 3',
            'codigo_postal': '00000',
            'piso': 'Piso 3',
            'depto': 'Depto 3',
            'legajo_id': 3
        }
    ]

    for data in clientes_data:
        db.session.add(Cliente(**data))
        db.session.commit()