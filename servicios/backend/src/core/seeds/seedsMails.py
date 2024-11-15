from datetime import datetime
from servicios.backend.src.core.services.servicioMail import crear_mail
from models.legajos.legajo import Legajo
from models.base import db

def seeds_mails():
    seed_mails()

def seed_mails():
    # Crear legajo provisional
    legajo_provisional = Legajo()
    db.session.add(legajo_provisional)
    db.session.commit()

    mails_data = [
        {
            'fecha': datetime(2023, 1, 1),
            'nombre_archivo': 'mail1.pdf',
            'legajo_id': legajo_provisional.id
        },
        {
            'fecha': datetime(2023, 2, 1),
            'nombre_archivo': 'mail2.pdf',
            'legajo_id': legajo_provisional.id
        },
        {
            'fecha': datetime(2023, 3, 1),
            'nombre_archivo': 'mail3.pdf',
            'legajo_id': legajo_provisional.id
        }
    ]

    for data in mails_data:
        crear_mail(data, data['legajo_id'])

