from models import db
from models.mails.mail import Mail
from datetime import datetime

def crear_mail(data, legajo_id):
    nuevo_mail = Mail(
        fecha=datetime.now(),
        nombre_archivo=data.get('nombre_archivo'),
        legajo_id=legajo_id
    )
    db.session.add(nuevo_mail)
    db.session.commit()
    return nuevo_mail

def listar_mails():
    mails = Mail.query.all()
    return mails