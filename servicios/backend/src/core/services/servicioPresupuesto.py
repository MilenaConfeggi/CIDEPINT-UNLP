from models import db
from models.presupuestos.STAN import STAN
from models.presupuestos.mediodepago import MedioPago
from models.presupuestos.ensayo import Ensayo
from models.presupuestos.ensayo_stan import EnsayoStan
from models.presupuestos.presupuesto_stan import PresupuestoStan
from models.presupuestos.presupuesto import Presupuesto


def crear_stan(data):
    stan = STAN(
        numero=data.get('numero'),
        precio_pesos=data.get('precio_pesos'),
        precio_dolares=data.get('precio_dolares'),
        precio_por_muestra=data.get('precio_por_muestra'),
    )

    db.session.add(stan)
    db.session.commit()
    return stan

def crear_ensayo(nombre):
    ensayos = listar_ensayos()
    for ensayo in ensayos:
        if ensayo.nombre == nombre:
            return ensayo
    ensayo = Ensayo(
        nombre=nombre
    )

    db.session.add(ensayo)
    db.session.commit()
    return ensayo

def crear_ensayo_stan(ensayo_id, stan_id):
    ensayo_stan = EnsayoStan(
        ensayo_id=ensayo_id,
        stan_id=stan_id
    )

    db.session.add(ensayo_stan)
    db.session.commit()

def listar_stans():
    return STAN.query.all()

def listar_ensayos():
    return Ensayo.query.all()

def listar_ensayos_para_stan(id_stan):
    ensayos = db.session.query(Ensayo).join(EnsayoStan).filter(EnsayoStan.stan_id == id_stan).all()
    return ensayos