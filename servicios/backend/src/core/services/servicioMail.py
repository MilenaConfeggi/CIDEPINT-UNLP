from models import db
from models.mails.mail import Mail
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def crear_mail(data, legajo_id):
    nuevo_mail = Mail(
        fecha=datetime.now(),
        nombre_archivo=data.get('nombre_archivo'),
        legajo_id=legajo_id
    )
    db.session.add(nuevo_mail)
    db.session.commit()
    return nuevo_mail

def validar_tipo(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validar_nombre(filename, id_legajo):
    mails = Mail.query.filter_by(legajo_id=id_legajo).all()
    for mail in mails:
        if mail.nombre_archivo == filename:
            return False
    return True

def listar_mails(nro_legajo):
    mails = Mail.query.filter_by(legajo_id=nro_legajo).all()
    return mails

def eliminar_mail(id_mail):
    mail = Mail.query.get(id_mail)
    db.session.delete(mail)
    db.session.commit()
    return mail