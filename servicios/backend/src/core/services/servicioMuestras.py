from flask_jwt_extended import get_jwt_identity, jwt_required
from models import db
from models.muestras.muestra import Muestra
from models.muestras.foto import Foto
from models.usuarios.usuario import Usuario
from models.legajos.legajo import Legajo
from models.personal.empleado import Empleado
from datetime import datetime


def crear_muestra(data, legajo_id):
    # Crear una nueva muestra con los datos proporcionados por el usuario
    nueva_muestra = Muestra(
        nro_muestra=data.get('nro_muestra'),  # Número de muestra ingresado por el usuario
        nro_grupo=data.get('nro_grupo'),  # Número de grupo ingresado por el usuario (opcional)
        fecha_ingreso=data.get('fecha_ingreso'),  # Fecha de ingreso proporcionada
        iden_cliente=data.get('iden_cliente'),  # Identificación del cliente proporcionada
        terminada=False,  # Por defecto, la muestra no está terminada
        legajo_id=legajo_id  # Asociar la muestra al legajo correspondiente
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
    if fecha > datetime.now().date():
        return False
    return True

def crear_foto(data, muestra_id):
    nueva_foto = Foto(
        nombre_archivo=data.get('nombre_archivo'),
        fecha=data.get('fecha'),
        descripcion=data.get('descripcion'),
        muestra_id=muestra_id
    )
    db.session.add(nueva_foto)
    db.session.commit()
    print("nueva foto", nueva_foto)
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


def tiene_permiso(id_legajo, mail):
    legajo = Legajo.query.filter_by(id=id_legajo).first()
    usuario = Usuario.query.filter_by(mail=mail).first()
    for empleado in usuario.empleado:
        if empleado.area == legajo.area:
            return True
    return False

def hay_muestra_legajo(legajo_id):
    return Muestra.query.filter_by(legajo_id=legajo_id).first()

def obtener_foto(id_foto):
    return Foto.query.get(id_foto)

def eliminar_foto(id_foto):
    foto = Foto.query.get(id_foto)
    db.session.delete(foto)
    db.session.commit()

def obtener_ultima_muestra():
    # Obtener la última muestra cargada al sistema (por ID, que refleja el orden de inserción)
    ultima_muestra = Muestra.query.order_by(Muestra.id.desc()).first()
    if ultima_muestra:
        # Formatear el número como "nrodemuestra-nrodegrupo"
        nro_grupo = f"-{ultima_muestra.nro_grupo}" if ultima_muestra.nro_grupo else ""
        return f"{ultima_muestra.nro_muestra}{nro_grupo}"
    return None

def obtener_muestra(id_muestra):
    return Muestra.query.get(id_muestra)

def eliminar_muestra(id_muestra):
    muestra = Muestra.query.get(id_muestra)
    if muestra:
        db.session.delete(muestra)
        db.session.commit()