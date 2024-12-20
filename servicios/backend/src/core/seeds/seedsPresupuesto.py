from models.presupuestos.STAN import STAN
from models.base import db
from models.presupuestos.ensayo import Ensayo
from models.presupuestos.ensayo_stan import EnsayoStan
from servicios.backend.src.core.services.servicioPresupuesto import crear_stan, crear_ensayo, crear_ensayo_stan, crear_presupuesto, crear_medio_pago
from models.legajos.legajo import Legajo
from models.clientes.cliente import Cliente
from models.legajos import create_legajo, find_legajo_by_id
from datetime import datetime
from models.presupuestos.presupuesto import Presupuesto
from models.presupuestos.presupuesto_stan import PresupuestoStan

def seeds_presupuestos():
    presupuestos_data = [
        {
            "fecha_creacion": datetime(2024, 1, 1),
            "precio": 1000,
            "medio_de_pago_id": 1,
            "nro_presupuesto": 1,
            "legajo_id": 33,
        },
        {
            "fecha_creacion": datetime(2024, 1, 1),
            "precio": 2000,
            "medio_de_pago_id": 2,
            "nro_presupuesto": 2,
            "legajo_id": 34,
        },
        {
            "fecha_creacion": datetime(2024, 2, 1),
            "precio": 3000,
            "medio_de_pago_id": 3,
            "nro_presupuesto": 3,
            "legajo_id": 35,
        },
        {
            "fecha_creacion": datetime(2024, 3, 1),
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
