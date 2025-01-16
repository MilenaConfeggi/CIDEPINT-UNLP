from models import db
from models.interarea.interarea import Interarea
from models.interarea.estadoInterarea import EstadoInterarea
from models.muestras.muestra import Muestra
from datetime import datetime

def crear_interarea(data):
    # Crear la instancia de Interarea
    nueva_interarea = Interarea(
        fecha_creacion=datetime.now(),
        fecha_solicitud_firmada=None,
        nombre_archivo=data.get('nombre_archivo'),
        investigacion=data.get('investigacion'),
        nro_interarea=generarNroInterarea(),
        nro_investigacion=data.get('nro_investigacion'),
        estadoInterarea_id=data.get('estadoInterarea_id'),
        legajo_id=data.get('legajo_id'),
        area_receptora_id=data.get('area_receptora_id'),
        area_solicitante_id=data.get('area_solicitante_id'),
        muestra_investigacion=data.get('muestra_investigacion')
    )

    muestra_ids = data.get('muestra_id', []) 
    if muestra_ids:
        muestras = Muestra.query.filter(Muestra.id.in_(muestra_ids)).all()
        nueva_interarea.muestras.extend(muestras)

    db.session.add(nueva_interarea)
    db.session.commit()

    return nueva_interarea


def crear_estadoInterarea(nombre):
    nuevo_estado = EstadoInterarea(
        nombre= nombre
    )
    db.session.add(nuevo_estado)
    db.session.commit()

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

def guardar_resultado(id, data):
    interarea = obtener_interarea(id)
    interarea.estadoInterarea_id = data.get('estadoInterarea_id')
    interarea.resultados = data.get('resultados')
    db.session.commit()
    return interarea

def cargar_solicitud_completa(id):
    interarea = obtener_interarea(id)
    interarea.estadoInterarea_id = 1
    db.session.commit()
    return interarea

def cargar_solicitud_firmada(id, newFileName):
    interarea = obtener_interarea(id)
    interarea.fecha_solicitud_firmada = datetime.now()
    interarea.estadoInterarea_id = 2
    interarea.nombre_archivo = newFileName
    db.session.commit()
    return interarea
