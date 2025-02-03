from models.base import db
from models.documentos.estado import Estado
from models.documentos.tipo_documento import Tipo_Documento
from models.documentos.documento import Documento
from models.legajos.legajo import Legajo
from datetime import datetime
from models.personal.area import Area
from models.clientes.cliente import Cliente
from models.presupuestos.ensayo import Ensayo
from models.presupuestos.STAN import STAN
from models.presupuestos.presupuesto import Presupuesto
from sqlalchemy import func

def create_estado(data):
    if find_estado_by_nombre(data["nombre"]) is not None:
        return None
    estado = Estado(**data)
    db.session.add(estado)
    db.session.commit()
    return estado


def listar_documentos(
    page=1,
    per_page=10,
    tipo_documento=None,
    empresa=None,
    fecha=None,
    area=None,
    ensayo=None,
):
    tipo_documento = tipo_documento.strip()
    query = db.session.query(Documento)
    query = query.join(Legajo.documento)
    if tipo_documento:
        query = query.filter_by(tipo_documento_id=tipo_documento)
    if empresa:
        query = query.join(Legajo.cliente).filter(Cliente.nombre.like(f"%{empresa}%"))
    if fecha:
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
        query = query.filter(func.date(Documento.fecha_creacion) == fecha.date())
    if area:
        query = query.join(Legajo.area).filter(Area.id == area)
    if ensayo:
        query = query.join(Presupuesto, Legajo.presupuesto_cidepint)
        query = query.join(STAN, Presupuesto.stans)
        query = query.join(Ensayo, STAN.ensayos).filter(
            Ensayo.nombre.like(f"%{ensayo}%")
        )
    query = query.order_by(Documento.fecha_creacion.desc())
    return query.paginate(page=page, per_page=per_page, error_out=False)


def list_estados():
    return db.session.query(Estado).all()


def find_estado_by_nombre(nombre):
    return db.session.query(Estado).filter_by(nombre=nombre).first()


def listar_tipos_documentos():
    return db.session.query(Tipo_Documento).all()


def get_tipo_documento(id):
    return db.session.query(Tipo_Documento).filter_by(id=id).first()


def get_tipo_documento_nombre(nombre):
    return db.session.query(Tipo_Documento).filter_by(nombre=nombre).first()


def create_tipo_documento(data):
    if get_tipo_documento(data["id"]) is not None:
        return None
    tipo_documento = Tipo_Documento(**data)
    db.session.add(tipo_documento)
    db.session.commit()
    return tipo_documento


def get_documento(id):
    return db.session.query(Documento).filter_by(id=id).first()


def find_documento(data):
    query = Documento.query
    if data["nombre_documento"] is not None:
        query = query.filter_by(nombre_documento=data["nombre_documento"])
    query = query.filter_by(tipo_documento_id=data["tipo_documento_id"])
    query = query.filter_by(legajo_id=data["legajo_id"])
    return query.first()


def find_documento_by_id(id):
    return db.session.query(Documento).filter_by(id=id).first()


def create_documento(data):
    if find_documento(data) is not None:
        return None
    documento = Documento(**data)
    db.session.add(documento)
    db.session.commit()
    return documento


def list_legajos(page=1, per_page=10, empresa=None, fecha=None, area=None):
    empresa = empresa.strip()
    fecha = fecha.strip()
    area = area.strip()
    query = Legajo.query
    if empresa:
        query = query.join(Legajo.cliente).filter(Cliente.email.like(f"%{empresa}%"))
    if fecha:
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
        print(fecha)
        query = query.filter(Legajo.fecha_entrada == fecha)
    if area:
        query = query.join(Legajo.area).filter(Area.id == area)
    return query

def list_documentos_by_tipo(tipo):
    return db.session.query(Documento).filter_by(tipo_documento_id=tipo).all()

def list_documentos_adicionales_by_legajo(legajo):
    return db.session.query(Documento).filter_by(legajo_id=legajo, tipo_documento_id=8).all()