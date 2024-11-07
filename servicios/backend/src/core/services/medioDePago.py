from models import MedioDePago, db

def crearMedioDePago(nombre):
    medio_de_pago = {
        "medio_de_pago": nombre
    }
    medioDePago = MedioDePago(medio_de_pago)
    db.session.add(medioDePago)
    db.session.commit()
