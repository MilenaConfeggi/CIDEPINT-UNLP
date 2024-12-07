from models.compras.compra import Compra
from sqlalchemy.orm import joinedload

def buscar_compra(id_compra):
    return Compra.query.filter(Compra.id == id_compra).first()

def filtrar_compras(fecha_menor, fecha_mayor, estado, tipo, area, page, per_page):
    query = Compra.query
    if fecha_menor and fecha_mayor:
        query = query.filter(Compra.fecha >= fecha_menor, Compra.fecha <= fecha_mayor)
    if fecha_menor and not fecha_mayor:
        query = query.filter(Compra.fecha >= fecha_menor)
    if not fecha_menor and fecha_mayor:
        query = query.filter(Compra.fecha <= fecha_mayor)
    if not estado:
        query = query.filter(Compra.estado != "CANCELADA")
    if tipo == "Personal":
        query = query.join(Compra.solicitante).filter(Compra.solicitante.has(area_id=area))
    return query.order_by(Compra.fecha.asc()).paginate(page=page,per_page=per_page,error_out=False)
    
def filtrar_compras_descargadas(fecha_menor, fecha_mayor, estado, tipo, area):
    query = Compra.query.options(
        joinedload(Compra.fondos),
        joinedload(Compra.empleados),
        joinedload(Compra.areas)
    )
    if fecha_menor and fecha_mayor:
        query = query.filter(Compra.fecha >= fecha_menor, Compra.fecha <= fecha_mayor)
    if fecha_menor and not fecha_mayor:
        query = query.filter(Compra.fecha >= fecha_menor)
    if not fecha_menor and fecha_mayor:
        query = query.filter(Compra.fecha <= fecha_mayor)
    if not estado:
        query = query.filter(Compra.estado != "CANCELADA")
    if tipo == "Personal":
        query = query.join(Compra.solicitante).filter(Compra.solicitante.has(area_id=area))
    return query.order_by(Compra.fecha.asc()).all()
