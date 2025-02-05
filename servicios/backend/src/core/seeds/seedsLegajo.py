from datetime import datetime
from models.legajos.legajo import Legajo
from models.clientes.cliente import Cliente
from models.legajos import create_legajo, find_legajo_by_id
from models.base import db
from models.presupuestos.presupuesto import Presupuesto
from models.presupuestos.presupuesto_stan import PresupuestoStan


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
