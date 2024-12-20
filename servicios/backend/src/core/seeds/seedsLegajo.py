from datetime import datetime
from models.legajos.legajo import Legajo
from models.clientes.cliente import Cliente
from models.legajos import create_legajo, find_legajo_by_id
from models.clientes import find_cliente_by_mail
from models.base import db
from models.presupuestos.presupuesto import Presupuesto
from models.presupuestos.presupuesto_stan import PresupuestoStan

"""""
def seeds_presupuestos():
    presupuestos_data = [
        {
            "fecha_carga": datetime(2024, 1, 1),
            "precio": 1000,
            "medio_de_pago_id": 1,
            "nro_presupuesto": 1,
            "legajo_id": 33,
        },
        {
            "fecha_carga": datetime(2024, 1, 1),
            "precio": 2000,
            "medio_de_pago_id": 2,
            "nro_presupuesto": 2,
            "legajo_id": 34,
        },
        {
            "fecha_carga": datetime(2024, 2, 1),
            "precio": 3000,
            "medio_de_pago_id": 3,
            "nro_presupuesto": 3,
            "legajo_id": 35,
        },
        {
            "fecha_carga": datetime(2024, 3, 1),
            "precio": 4000,
            "medio_de_pago_id": 1,
            "nro_presupuesto": 4,
        },
    ]

    for data in presupuestos_data:
        db.session.add(Presupuesto(**data))
    db.session.commit()


def seeds_presupuestos_stan():
    presupuestos_stan_data = [
        {"presupuesto_id": 1, "stan_id": 1, "precio_carga": 1000},
        {"presupuesto_id": 2, "stan_id": 2, "precio_carga": 2000},
        {"presupuesto_id": 3, "stan_id": 3, "precio_carga": 3000},
    ]

    for data in presupuestos_stan_data:
        db.session.add(PresupuestoStan(**data))
    db.session.commit()
"""""

def seeds_legajos():
    legajos_data = [
        {
            "fecha_entrada": datetime(2024, 1, 1),
            "es_juridico": True,
            "necesita_facturacion": True,
            "objetivo": "Objetivo de legajo",
            "area_id": 1,
        },
        {
            "fecha_entrada": datetime(2024, 1, 1),
            "es_juridico": True,
            "necesita_facturacion": True,
            "objetivo": "Objetivo de legajo2",
            "area_id": 2,
        },
        {
            "fecha_entrada": datetime(2024, 2, 1),
            "es_juridico": False,
            "necesita_facturacion": False,
            "objetivo": "Objetivo de legajo3",
            "area_id": 3,
        },
        {
            "fecha_entrada": datetime(2024, 3, 1),
            "es_juridico": True,
            "necesita_facturacion": True,
            "objetivo": "Objetivo de legajo4",
            "area_id": 1,
        },
    ]
    for data in legajos_data:
        create_legajo(data)
    db.session.commit()
    #seeds_presupuestos()
    #seeds_presupuestos_stan()
