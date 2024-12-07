from servicios.backend.src.core.services.servicioInterarea import crear_interarea
from models.legajos.legajo import Legajo
from models.areas.area import Area
from models.base import db
from datetime import datetime
from servicios.backend.src.core.seeds.seedsMuestra import seed_muestras

def seeds_interarea():
    seed_interareas()

def seed_interareas():
    # Llamar a seed_muestras para obtener las muestras creadas
    muestras = seed_muestras()

    # Crear legajo y área provisionales
    legajo_provisional = Legajo()
    area_provisional = Area()
    db.session.add(legajo_provisional)
    db.session.add(area_provisional)
    db.session.commit()

    interareas_data = [
        {
            'fecha_creacion': datetime(2024, 10, 10),
            'fecha_solicitud_no_firmada': datetime(2024, 10, 10),
            'fecha_solicitud_firmada': datetime(2024, 11, 10),
            'nombre_solicitud_firmada': 'prueba1',
            'nombre_solicitud_no_firmada': 'prueba1.1',
            'investigacion': True,
            'nro_interarea': 1,
            'legajo_id': legajo_provisional.id,
            'area_id': area_provisional.id,
            'muestra_id': muestras[0].id
        },
        {
            'fecha_creacion': datetime(2024, 10, 11),
            'fecha_solicitud_no_firmada': datetime(2024, 10, 11),
            'fecha_solicitud_firmada': datetime(2024, 11, 11),
            'nombre_solicitud_firmada': 'prueba2',
            'nombre_solicitud_no_firmada': 'prueba2.1',
            'investigacion': False,
            'nro_interarea': 2,
            'legajo_id': legajo_provisional.id,
            'area_id': area_provisional.id,
            'muestra_id': muestras[1].id  # Asignar otra muestra
        },
        {
            'fecha_creacion': datetime(2024, 10, 11),
            'fecha_solicitud_no_firmada': datetime(2024, 10, 11),
            'fecha_solicitud_firmada': datetime(2024, 11, 11),
            'nombre_solicitud_firmada': 'prueba2',
            'nombre_solicitud_no_firmada': 'prueba2.1',
            'investigacion': False,
            'nro_interarea': 2,
            'legajo_id': legajo_provisional.id,
            'area_id': area_provisional.id,
            'muestra_id': muestras[2].id 
        }
    ]

    for data in interareas_data:
        crear_interarea(data, data['legajo_id'], data['area_id'], data['muestra_id'])

    