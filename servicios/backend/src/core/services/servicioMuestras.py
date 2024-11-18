from models import db
from models.muestras.muestra import Muestra
from models.muestras.foto import Foto
from datetime import datetime

def crear_muestra(data, legajo_id):
    anio_actual = datetime.now().year
    ultima_muestra = Muestra.query.filter(db.extract('year', Muestra.fecha_ingreso) == anio_actual).order_by(Muestra.nro_muestra.desc()).first()

    if (ultima_muestra):
        nro_muestra = ultima_muestra.nro_muestra + 1
    else:
        nro_muestra = 1
    nueva_muestra = Muestra(
        nro_muestra=nro_muestra,
        fecha_ingreso=data.get('fecha_ingreso'),
        iden_cliente=data.get('iden_cliente'),
        terminada= False,
        legajo_id=legajo_id
    )
    db.session.add(nueva_muestra)
    db.session.commit()
    return nueva_muestra


def listar_muestras(id_legajo):
    return Muestra.query.filter_by(legajo_id=id_legajo).all()

def terminar_muestra(id_muestra):
    muestra = Muestra.query.get(id_muestra)
    muestra.terminada = True
    db.session.commit()
    return muestra

def validar_identificacion_cliente(data, legajo_id):
    muestra = Muestra.query.filter_by(iden_cliente=data.get('iden_cliente'), legajo_id=legajo_id).first()
    if muestra:
        return False
    return True

def validar_entre_cargadas(muestras, muestra):
    for elem in muestras:
        if elem.get('iden_cliente') == muestra.get('iden_cliente'):
            return False
    return True

def validar_longitud(muestra):
    if len(muestra.get('iden_cliente')) > 100:
        return False
    return True

def validar_fecha(muestra):
    if muestra.get('fecha_ingreso') > datetime.now().date():
        return False
    return True

def crear_foto(data, muestra_id):
    nueva_foto = Foto(
        nombre_archivo=data.get('nombre_archivo'),
        fecha=data.get('fecha'),
        muestra_id=muestra_id
    )
    db.session.add(nueva_foto)
    db.session.commit()
    return nueva_foto

def listar_fotos(id_muestra):
    return Foto.query.filter_by(muestra_id=id_muestra).all()

def listar_fotos_por_legajo(id_legajo):
    return Foto.query.join(Muestra).filter(Muestra.legajo_id == id_legajo).all()