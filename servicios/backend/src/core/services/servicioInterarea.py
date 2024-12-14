from models import db
from models.interarea.interarea import Interarea
from datetime import datetime

def crear_interarea(data):
    nueva_interarea = Interarea(
        fecha_creacion=datetime.now(),
        fecha_solicitud_no_firmada=datetime.now(),
        fecha_solicitud_firmada=None,
        nombre_solicitud_firmada=None,
        nombre_solicitud_no_firmada=data.get('nombre_solicitud_no_firmada'),
        investigacion=data.get('investigacion'),
        nro_interarea= generarNroInterarea(),
        legajo_id=data.get('legajo_id'),
        area_id=data.get('area_id'),
        muestra_id=data.get('muestra_id')
    )
    db.session.add(nueva_interarea)
    db.session.commit()
    return nueva_interarea

def listar_interareas():
    interareas = Interarea.query.all()
    return interareas

def obtener_interarea(id):
    interarea = Interarea.query.get(id)
    return interarea

def generarNroInterarea():
    ultima_interarea = Interarea.query.order_by(Interarea.id.desc()).first()
    ultima_id = ultima_interarea.id if ultima_interarea else 0
    fecha_actual = datetime.now().strftime("%d%m%Y")
    nro_interarea = f"{ultima_id}-{fecha_actual}"
    return nro_interarea

