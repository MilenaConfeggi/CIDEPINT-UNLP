from models.base import db
from models.legajos.legajo import Legajo
from models.documentos import find_estado_by_nombre
from models.clientes import Cliente
from datetime import datetime

def list_legajos(page=1, per_page=10, empresa=None, fecha=None,facturacion=None):
    
    
    query = Legajo.query
    if empresa:
        empresa = empresa.strip()
        query = query.join(Legajo.cliente).filter(Cliente.email.like(f'%{empresa}%'))
    if fecha:
        fecha = fecha.strip()
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
        query = query.filter(Legajo.fecha_entrada == fecha)
    if facturacion:
        query = query.filter(Legajo.necesita_facturacion)
    return query.paginate(page=page, per_page=per_page, error_out=False)

def list_legajos_all():
    return db.session.query(Legajo).all()

def create_legajo(data):
    if find_legajo_by_id(data['nro_legajo']):
        return None
    legajo = Legajo(**data)
    new_estado = find_estado_by_nombre('En curso')
    if new_estado is None:
        return None
    legajo.estado = new_estado
    db.session.add(legajo)
    db.session.commit()
    return legajo


def find_legajo_by_id(id):
    return db.session.query(Legajo).filter_by(id=id).first()