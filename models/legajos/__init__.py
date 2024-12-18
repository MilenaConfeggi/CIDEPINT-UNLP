from models.base import db
from models.legajos.legajo import Legajo
from models.documentos import find_estado_by_nombre
from models.clientes import Cliente
from models.personal.area import Area
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import contains_eager
from models.presupuestos.presupuesto import Presupuesto
from models.presupuestos.STAN import STAN
from models.presupuestos.ensayo import Ensayo


def list_legajos(page=1, per_page=10, empresa=None, fecha=None, area=None, ensayo=None):
    # empresa = empresa.strip()
    # fecha = fecha.strip()
    # area = area.strip()
    query = Legajo.query
    query = (
        Legajo.query.outerjoin(Legajo.presupuesto_cidepint)  
        .outerjoin(Presupuesto.stans) 
        .outerjoin(STAN.ensayos)
        .options(
            contains_eager(
                Legajo.presupuesto_cidepint
            )  
            .contains_eager(Presupuesto.stans) 
            .contains_eager(STAN.ensayos)
        )
    )
    if empresa:
        query = query.join(Legajo.cliente).filter(Cliente.nombre.like(f"%{empresa}%"))
    if fecha:
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
        query = query.filter(func.date(Legajo.fecha_entrada) == fecha.date()) 
    if area:
        query = query.join(Legajo.area).filter(Area.id == area)
    if ensayo:
        query = query.filter(Legajo.presupuesto_cidepint.any(STAN.ensayos.any(Ensayo.nombre.like(f"%{ensayo}%"))))
    return query.paginate(page=page, per_page=per_page, error_out=False)


def list_legajos_all():
    return db.session.query(Legajo).all()


def create_legajo(data):
    legajo = Legajo(**data)
    new_estado = find_estado_by_nombre("En curso")
    if new_estado is None:
        return None
    legajo.estado = new_estado
    db.session.add(legajo)
    db.session.commit()
    return legajo


def find_legajo_by_id(id):

    return db.session.query(Legajo).filter_by(id=id).first()


def find_mail_legajo(id):
    return db.session.query(Legajo).filter_by(id=id).first().cliente.email
