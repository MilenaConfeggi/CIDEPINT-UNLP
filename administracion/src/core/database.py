from models import db

def reset():
    """
    Resetea la base de datos
    """

    db.drop_all()
    db.create_all()
