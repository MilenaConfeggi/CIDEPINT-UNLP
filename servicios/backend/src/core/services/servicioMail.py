from models import db
from models.mails.mail import Mail

def crear_mail(data, legajo_id):
    nuevo_mail = Mail(
        fecha=data.get('fecha'),
        nombre_archivo=data.get('nombre_archivo'),
        legajo_id=legajo_id
    )
    db.session.add(nuevo_mail)
    db.session.commit()
    return nuevo_mail