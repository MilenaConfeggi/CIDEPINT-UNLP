from models.base import db
from models.Fondo.fondo import Fondo 

def listar_fondos():

    return Fondo.query.all()

def listar_fondos_activos():
    """
    Obtiene todos los fondos activos en la base de datos.

    Returns:
        List[Fondo]: Una lista de objetos Fondo activos.
    """
    return Fondo.query.filter_by(borrado=False).all()


def filtrar_fondos(page, per_page):
    return Fondo.query.filter_by(borrado=False).order_by(Fondo.titulo.asc()).paginate(page=page, per_page=per_page, error_out=False)


def conseguir_fondo_de_id(fondo_id):

    return Fondo.query.get(fondo_id)
def conseguir_fondo_por_nombre(nombre):
    """
    Obtiene un fondo por su nombre.
    Args:
        nombre (string): El nombre del fondo a buscar.
    Returns:
        Fondo: El objeto Fondo si se encuentra, de lo contrario, None.
    """
    return Fondo.query.filter_by(titulo=nombre, borrado=False).first()

def create_fondo(**kwargs):
    """
    Crea un nuevo Fondo en la base de datos

    Args:
        **kwargs: Los argumentos necesarios para crear el fondo, como campos clave-valor.

    Returns:
        Fondo: El objeto Fondo recién creado y guardado en la base de datos.
    """
    fondo = Fondo(**kwargs)
    db.session.add(fondo)
    db.session.commit()
    return fondo

def modificar_fondo(id, **kwargs):
    """
    Modifica un fondo existente en la base de datos.

    Busca el fondo por su ID(titulo) y, si existe, actualiza sus campos con los valores proporcionados.

    Args:
        id (striing): El titulo del fondo a modificar.
        **kwargs: Los nuevos valores de los campos a actualizar, como clave-valor.

    Returns:
        Fondo: El objeto Fondo actualizado si se encuentra, de lo contrario, None.
    """
    fondo = conseguir_fondo_de_id(id)
    if fondo:
        for key, value in kwargs.items():
            setattr(fondo, key, value)
        db.session.commit()
        return fondo
    return None 

def delete_fondo(id):
    """
    Realiza un borrado lógico de un Fondo por su ID, marcándolo como borrado.

    Args:
        id (string): El titulo del fondo que se desea borrar.

    Returns:
        Fondo: El objeto fondo con la marca de borrado aplicada si se encuentra,
        de lo contrario, None.
    """
    fondo = conseguir_fondo_de_id(id)
    if fondo:
        fondo.borrado = True
        db.session.commit()
        return fondo
    return None