from models import db
from models.muestras.muestra import Muestra
from models.muestras.foto import Foto
from datetime import datetime

NRO_MUESTRA_INICIAL = 5

def crear_muestra(data, legajo_id):
    fecha_ingreso = data.get('fecha_ingreso')
    anio_ingreso = fecha_ingreso.year

    # Verificar si hay alguna muestra en la base de datos
    ultima_muestra = Muestra.query.order_by(Muestra.fecha_ingreso.desc(), Muestra.nro_muestra.desc()).first()

    if not ultima_muestra:
        # No hay ninguna muestra en la base de datos
        nro_muestra = NRO_MUESTRA_INICIAL
    else:
        # Hay muestras en la base de datos
        ultima_muestra_anio_ingreso = Muestra.query.filter(db.extract('year', Muestra.fecha_ingreso) == anio_ingreso).order_by(Muestra.nro_muestra.desc()).first()
        
        if not ultima_muestra_anio_ingreso:
            # Es la primera muestra del año de ingreso
            nro_muestra = 1
        else:
            # Incrementar el número de muestra basado en la última muestra del año de ingreso
            nro_muestra = ultima_muestra_anio_ingreso.nro_muestra + 1

    nueva_muestra = Muestra(
        nro_muestra=nro_muestra,
        fecha_ingreso=data.get('fecha_ingreso'),
        iden_cliente=data.get('iden_cliente'),
        terminada=False,
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

def validar_fecha(fecha):
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    print(fecha)
    print(datetime.now().date())
    if fecha > datetime.now().date():
        print("entro")
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

def listar_fotos_por_fecha(legajo_id, fecha):
    return Foto.query.join(Muestra).filter(
        Muestra.legajo_id == legajo_id,
        Foto.fecha == fecha
    ).all()

def listar_todas():
    return Muestra.query.all()