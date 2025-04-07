from datetime import datetime
from models.clientes.cliente import Cliente
from models.base import db
from models.clientes import create_cliente
def seeds_clientes():
    legajos_id = [16837, 16838, 16839, 16840]
    clientes_data = [
        {
            'email': 'milenaconfeggi@gmail.com',
            'cuit': '1',
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
            'nombre': 'Cliente 1'
        },
        {
            'email': 'cliente2@mail.com',
            'cuit': '2',
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
            'nombre': 'Cliente 2',

        },
        {
            'email': 'cliente3@mail.com',
            'cuit': '3',
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
            'nombre': 'Cliente 3'

        },
        {
            'email': 'cliente4@mail.com',
            'cuit': '4',
            'telefono': '123456789',
            'celular': '123456789',
            'direccion': 'Calle 4',
            'fecha_nacimiento': datetime(1990, 1, 1),
            'contacto': 'Contacto 4',
            'calle': 'Calle 4',
            'numero': '4',
            'localidad': 'Localidad 4',
            'codigo_postal': '00000',
            'piso': 'Piso 4',
            'depto': 'Depto 4',
            'nombre': 'Cliente 4'

        },
    ]

    for i in range(4):
        create_cliente(clientes_data[i], legajos_id[i])
    db.session.commit()