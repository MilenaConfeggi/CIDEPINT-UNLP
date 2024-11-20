from models.base import db
from models.patrimonio.bien import Bien

def listar_bienes():

    return Bien.query.all()


def conseguir_bien_de_id(bien_id):

    return Bien.query.get(bien_id)


def crear_bien(
    titulo,
    numero_inventario,
    anio,
    institucion,
    descripcion,
):
    nuevo_bien = Bien(
            titulo=titulo,
            numero_inventario=numero_inventario,
            anio=anio,
            institucion=institucion,
            descripcion=descripcion,
            )
    
    db.session.add(nuevo_bien)
    db.session.commit()
    
    return nuevo_bien


def filtrar_bienes(titulo, numero_inventario, area, page, per_page):
    query = Bien.query

    if titulo:
        query = query.filter(Bien.titulo.ilike(f"{titulo}%"))
    if numero_inventario:
        query = query.filter(Bien.numero_inventario.ilike(f"{numero_inventario}%"))
    
    return query.order_by(Bien.titulo.asc()).paginate(page=page,per_page=per_page,error_out=False)