from models import db
from models.interarea.interarea import Interarea

def crear_interarea(data, legajo_id, area_id, muestra_id):
    nueva_interarea = Interarea(
        fecha_creacion=data.get('fecha_creacion'),
        fecha_solicitud_no_firmada=data.get('fecha_solicitud_no_firmada'),
        fecha_solicitud_firmada=data.get('fecha_solicitud_firmada'),
        nombre_solicitud_firmada=data.get('nombre_solicitud_firmada'),
        nombre_solicitud_no_firmada=data.get('nombre_solicitud_no_firmada'),
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

