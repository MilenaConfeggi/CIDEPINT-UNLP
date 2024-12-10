from models import db
from models.interarea.interarea import Interarea
from datetime import datetime

def crear_interarea(data, legajo_id, area_id, muestra_id):
    nueva_interarea = Interarea(
        fecha_creacion=datetime.now(),
        fecha_solicitud_no_firmada=datetime.now(),
        fecha_solicitud_firmada=None,
        nombre_solicitud_firmada=None,
        nombre_solicitud_no_firmada=None,
        investigacion=data.get('investigacion'),
        nro_interarea=data.get('nro_interarea'),
        legajo_id=legajo_id,
        area_id=area_id,
        muestra_id=muestra_id
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

