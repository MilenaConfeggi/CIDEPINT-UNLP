from datetime import datetime
from servicios.backend.src.core.services.servicioMuestras import crear_muestra, crear_foto
from models.legajos.legajo import Legajo
from models.base import db

def seeds_muestras():
    seed_muestras()
    seed_fotos()

def seed_muestras():
    # Crear legajo provisional
    legajo_provisional = Legajo()
    db.session.add(legajo_provisional)
    db.session.commit()

    muestras_data = [
        {
            'fecha_ingreso': datetime(2024, 1, 1),
            'iden_cliente': 'Muestra 1',
            'legajo_id': legajo_provisional.id,
            "terminada": False
        },
        {
            'fecha_ingreso': datetime(2024, 2, 1),
            'iden_cliente': 'Muestra 2',
            'legajo_id': legajo_provisional.id,
            "terminada": False
        },
        {
            'fecha_ingreso': datetime(2024, 3, 1),
            'iden_cliente': 'Muestra 3',
            'legajo_id': legajo_provisional.id,
            "terminada": False
        }
    ]

    muestras_creadas = []
    for data in muestras_data:
        muestra = crear_muestra(data, data['legajo_id'])
        muestras_creadas.append(muestra)
    return muestras_creadas

def seed_fotos():
    fotos_data = [
        {
            'nombre_archivo': 'foto1.jpg',
            'fecha': datetime(2023, 1, 2),
            'muestra_id': 1
        },
        {
            'nombre_archivo': 'foto2.jpg',
            'fecha': datetime(2023, 2, 2),
            'muestra_id': 1
        },
        {
            'nombre_archivo': 'foto3.jpg',
            'fecha': datetime(2023, 3, 2),
            'muestra_id': 3
        }
    ]

    for data in fotos_data:
        crear_foto(data, data['muestra_id'])
