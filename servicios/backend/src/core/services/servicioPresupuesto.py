from models import db
from models.presupuestos.STAN import STAN
from models.presupuestos.mediodepago import MedioPago
from models.presupuestos.ensayo import Ensayo
from models.presupuestos.ensayo_stan import EnsayoStan
from models.presupuestos.presupuesto_stan import PresupuestoStan
from models.presupuestos.presupuesto import Presupuesto

def crearTodo():
    crearMedioDePago("Efectivo")
    crearEnsayo("Ensayo 1")
    crearEnsayo("Ensayo 2")
    crearSTAN("STAN 1", "Descripcion STAN 1", 1000)
    crearSTAN("STAN 2", "Descripcion STAN 2", 2000)
    crearEnsayoSTAN(1, 1)
    crearEnsayoSTAN(1, 2)
    crearEnsayoSTAN(2, 1)
    crearEnsayoSTAN(2, 2)
    crearPresupuesto(1, "2021-01-01", 3000, 1)
    crearPresupuestoSTAN(1, 1, 1000)
    crearPresupuestoSTAN(1, 2, 2000)
    crearPresupuesto(2, "2021-01-02", 4000, 1)
    crearPresupuestoSTAN(2, 1, 1000)
    crearPresupuestoSTAN(2, 2, 2000)


def crearMedioDePago(nombre):
    medioDePago = MedioPago(medio_de_pago=nombre)
    db.session.add(medioDePago)
    db.session.commit()

def crearEnsayo(nombre):
    ensayo = Ensayo(nombre=nombre)
    db.session.add(ensayo)
    db.session.commit()

def crearSTAN(nombre, descripcion, precio):
    stan = STAN(nombre=nombre, descripcion=descripcion, precio=precio)
    db.session.add(stan)
    db.session.commit()

def crearEnsayoSTAN(ensayo_id, stan_id):
    ensayo_stan = EnsayoStan(ensayo_id=ensayo_id, stan_id=stan_id)
    db.session.add(ensayo_stan)
    db.session.commit()

def crearPresupuesto(nro_presupuesto, fecha_carga, precio, medio_de_pago_id):
    presupuesto = Presupuesto(nro_presupuesto=nro_presupuesto, fecha_carga=fecha_carga, precio=precio, medio_de_pago_id=medio_de_pago_id)
    db.session.add(presupuesto)
    db.session.commit()

def crearPresupuestoSTAN(presupuesto_id, stan_id, precio_carga):
    presupuesto_stan = PresupuestoStan(presupuesto_id=presupuesto_id, stan_id=stan_id, precio_carga=precio_carga)
    db.session.add(presupuesto_stan)
    db.session.commit()