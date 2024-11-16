from models import db
from models.muestras.muestra import Muestra
from models.muestras.foto import Foto

def crear_muestra(data, legajo_id):
    nueva_muestra = Muestra(
        nro_muestra=data.get('nro_muestra'),
        fecha_ingreso=data.get('fecha_ingreso'),
        iden_cliente=data.get('iden_cliente'),
        legajo_id=legajo_id
    )
    db.session.add(nueva_muestra)
    db.session.commit()
    return nueva_muestra

def crear_foto(data, muestra_id):
    nueva_foto = Foto(
        nombre_archivo=data.get('nombre_archivo'),
        fecha=data.get('fecha'),
        muestra_id=muestra_id
    )
    db.session.add(nueva_foto)
    db.session.commit()
    return nueva_foto

def listar_muestras(id_legajo):
    return Muestra.query.filter_by(legajo_id=id_legajo).all()

def listar_fotos():
    return Foto.query.all()
