from servicios.backend.src.core.services.servicioInterarea import crear_interarea
from models.legajos.legajo import Legajo
from models.personal.area import Area
from models.muestras.muestra import Muestra
from models.base import db

def seeds_interarea():
    seed_interareas()

def seed_interareas():
    muestras = Muestra.query.all()
    legajo_provisional = Legajo.query.all()
    area_provisional = Area.query.all()

    interareas_data = [
        {
            'nombre_archivo': 'prueba1.1',
            'investigacion': True,
            'nro_investigacion': '123',
            'estadoInterarea_id': 1,
            'legajo_id': None,
            'area_id': area_provisional[0].id,
            'muestra_id': muestras[0].id
        },
        {
            'nombre_archivo': 'prueba2.1',
            'investigacion': False,
            'nro_investigacion': None,
            'estadoInterarea_id': 1,
            'legajo_id': legajo_provisional[1].id,
            'area_id': area_provisional[1].id,
            'muestra_id': muestras[1].id
        },
        {
            'nombre_archivo': 'prueba2.1',
            'investigacion': False,
            'nro_investigacion': None,
            'estadoInterarea_id': 1,
            'legajo_id': legajo_provisional[2].id,
            'area_id': area_provisional[2].id,
            'muestra_id': muestras[2].id 
        }
    ]

    for data in interareas_data:
        crear_interarea(data)

    