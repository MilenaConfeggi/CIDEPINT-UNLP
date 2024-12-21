from models.presupuestos.mediodepago import MedioPago
from models.base import db

def seeds_medio_pago():
    medio_pago_data = [
        {
            'medio_de_pago': 'efectivo'
        },
        {
            'medio_de_pago': 'credito'
        },
        {
            'medio_de_pago': 'transferencia'
        },
        {
            'medio_de_pago': 'debito'
        }
    ]

    for data in medio_pago_data:
        db.session.add(MedioPago(**data))    
    db.session.commit()