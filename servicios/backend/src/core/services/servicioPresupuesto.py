from models import db
from models.presupuestos.STAN import STAN
from models.presupuestos.mediodepago import MedioPago
from models.presupuestos.ensayo import Ensayo
from models.presupuestos.ensayo_stan import EnsayoStan
from models.presupuestos.presupuesto_stan import PresupuestoStan
from models.presupuestos.presupuesto import Presupuesto


def crear_stan(numero, precio_pesos, precio_dolares):
    stan = STAN(
        numero=numero,
        precio_pesos=precio_pesos,
        precio_dolares=precio_dolares
    )

    db.session.add(stan)
    db.session.commit()

def crear_ensayo(nombre):
    ensayo = Ensayo(
        nombre=nombre
    )

    db.session.add(ensayo)
    db.session.commit()

def crear_ensayo_stan(ensayo_id, stan_id):
    ensayo_stan = EnsayoStan(
        ensayo_id=ensayo_id,
        stan_id=stan_id
    )

    db.session.add(ensayo_stan)
    db.session.commit()