from models.presupuestos.STAN import STAN
from models.base import db
from models.presupuestos.ensayo import Ensayo
from models.presupuestos.ensayo_stan import EnsayoStan
from servicios.backend.src.core.services.servicioPresupuesto import crear_stan, crear_ensayo, crear_ensayo_stan
def seeds_stans():
    seed_stan()
    seed_ensayos()
    seed_ensayos_stans()

def seed_stan():
    stan_data = [
        {
            'numero': '1',
            'precio_pesos': 1000,
            'precio_dolares': 100,
            "precio_por_muestra": True
        },
        {
            'numero': '2',
            'precio_pesos': 2000,
            'precio_dolares': 200,
            "precio_por_muestra": False
        },
        {
            'numero': '3',
            'precio_pesos': 3000,
            'precio_dolares': 300,
            "precio_por_muestra": True
        }
    ]

    for data in stan_data:
        crear_stan(data)

def seed_ensayos():
    ensayos_data = [
        {
            'nombre': 'Ensayo 1'
        },
        {
            'nombre': 'Ensayo 2'
        },
        {
            'nombre': 'Ensayo 3'
        }
    ]

    for data in ensayos_data:
        crear_ensayo(data['nombre'])

def seed_ensayos_stans():
    ensayos_stans_data = [
        {
            'ensayo_id': 1,
            'stan_id': 1
        },
        {
            'ensayo_id': 2,
            'stan_id': 2
        },
        {
            'ensayo_id': 3,
            'stan_id': 3
        }
    ]

    for data in ensayos_stans_data:
        crear_ensayo_stan(data['ensayo_id'], data['stan_id'])