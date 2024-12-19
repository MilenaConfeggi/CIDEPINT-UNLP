from models import db
from models.presupuestos.STAN import STAN
from models.presupuestos.mediodepago import MedioPago
from models.presupuestos.ensayo import Ensayo
from models.presupuestos.ensayo_stan import EnsayoStan
from models.presupuestos.presupuesto_stan import PresupuestoStan
from models.presupuestos.presupuesto import Presupuesto
from models.presupuestos.mediodepago import MedioPago
import re

def buscar_stan(id):
    return STAN.query.get(id)

def crear_stan(data):
    stan = STAN(
        numero= "STAN " + data.get('numero'),
        precio_pesos=data.get('precio_pesos'),
        precio_dolares=data.get('precio_dolares'),
        precio_por_muestra=data.get('precio_por_muestra'),
    )

    if validar_numero_stan(stan.numero) == False:
        return None
    
    db.session.add(stan)
    db.session.commit()
    return stan

def validar_numero_stan(numero):
    stan = STAN.query.filter_by(numero=numero).first()
    if stan is not None:
        return False
    return True

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

    def extract_number(stan):
        match = re.search(r'\d+', stan.numero)
        return int(match.group()) if match else float('inf')

    stans = STAN.query.all()
    stans.sort(key=extract_number)
    return stans

def listar_ensayos():
    return Ensayo.query.all()

def listar_ensayos_para_stan(id_stan):
    ensayos = db.session.query(Ensayo).join(EnsayoStan).filter(EnsayoStan.stan_id == id_stan).all()
    return ensayos

def modificar_precio_stan(id_stan, data):
    stan = STAN.query.get(id_stan)
    stan.precio_pesos = data.get('precio_pesos')
    stan.precio_dolares = data.get('precio_dolares')
    db.session.commit()

def crear_presupuesto(data):
    presupuesto = Presupuesto(
        precio=data.get('precio'),
        legajo=data.get('legajo'),
        medio_de_pago_id=data.get('medio_de_pago_id'),
    )
    db.session.add(presupuesto)
    db.session.commit()
    return presupuesto

def crear_presupuesto_stan(presupuesto, stan_id):
    presupuesto_stan = PresupuestoStan(
        presupuesto_id=presupuesto_id,
        stan_id=stan_id
    )

    db.session.add(presupuesto_stan)
    db.session.commit()
    return presupuesto

def crear_medio_pago(name):
    medio_pago = MedioPago(
        nombre = name
    )
    db.session.add(medio_pago)
    db.session.commit()
    return medio_pago