from models.presupuestos.STAN import STAN
from models.base import db
from models.presupuestos.ensayo import Ensayo
from models.presupuestos.ensayo_stan import EnsayoStan
from servicios.backend.src.core.services.servicioPresupuesto import crear_stan, crear_ensayo, crear_ensayo_stan, crear_presupuesto, crear_medio_pago
from models.legajos.legajo import Legajo
from models.clientes.cliente import Cliente
from models.legajos import create_legajo, find_legajo_by_id
from datetime import datetime


def seeds_presupuesto():

    stan4 = crear_stan(
        {
            'numero': '4',
            'precio_pesos': 4001,
            'precio_dolares': 500,
            "precio_por_muestra": True
        }
    )
    stan5 = crear_stan(
        {
            'numero': '5',
            'precio_pesos': 6000,
            'precio_dolares': 700,
            "precio_por_muestra": False
        }
    )
    stan6 = crear_stan(
        {
            'numero': '6',
            'precio_pesos': 900,
            'precio_dolares': 30,
            "precio_por_muestra": True
        }
    )

    ensayo4 = crear_ensayo('Ensayo 4')
    ensayo5 = crear_ensayo('Ensayo 5')
    ensayo6 = crear_ensayo('Ensayo 7')


    crear_ensayo_stan(ensayo4.id,stan4.id)
    crear_ensayo_stan(ensayo5.id,stan5.id)
    crear_ensayo_stan(ensayo6.id,stan6.id)

    legajo5 = create_legajo(
        {
            'fecha_entrada': datetime.now(),
            'nro_legajo': 'LEG5',
            'es_juridico': True,
            'necesita_facturacion': True,
            'objetivo': 'Localizado',
            'area_id': 2,
        }
    )
    legajo6 = create_legajo(
        {
            'fecha_entrada': datetime.now(),
            'nro_legajo': 'LEG6',
            'es_juridico': True,
            'necesita_facturacion': True,
            'objetivo': 'Objetivo de legajo',
            'area_id': 3,
        }
    )
    legajo7 = create_legajo(
        {
            'fecha_entrada': datetime.now(),
            'nro_legajo': 'LEG8',
            'es_juridico': False,
            'necesita_facturacion': False,
            'objetivo': 'Dominio total del mundo',
            'area_id': 1,
        }
    )

    medio_de_pago1 = crear_medio_pago("Efectivo")
    medio_de_pago2 = crear_medio_pago("Tarjeta")

    presupuesto1 = crear_presupuesto(
        {
            'precio': 488,
            'legajo': legajo5,
            'medio_de_pago_id': medio_de_pago1.id,
        }
    )

    presupuesto2 = crear_presupuesto(
        {
            'precio': 1656,
            'legajo': legajo6,
            'medio_de_pago_id': medio_de_pago2.id,
        }
    )

    presupuesto3 = crear_presupuesto(
        {
            'precio': 5458,
            'legajo': legajo7,
            'medio_de_pago_id': medio_de_pago1.id,
        }
    )