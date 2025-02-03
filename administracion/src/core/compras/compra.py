from models.compras.compra import Compra, estado_compra
from models.compras.compra_fondo import compra_fondo
from models.compras.compra_empleado import compra_empleado
from models.compras.compra_area import compra_area
from sqlalchemy.orm import joinedload
from models.base import db
from administracion.src.core.proveedores.proveedor import buscar_proveedor
from administracion.src.core.servicios.personal import conseguir_empleado_de_id, conseguir_area_de_id
from administracion.src.core.fondos.fondo import conseguir_fondo_de_id


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
    if tipo == "Personal":
        query = query.join(Compra.solicitante).filter(Compra.solicitante.has(area_id=area))
    if not estado:
        query = query.filter(Compra.estado != "CANCELADA")
    else:
        query = query.filter(Compra.estado == "CANCELADA")
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
    if tipo == "Personal":
        query = query.join(Compra.solicitante).filter(Compra.solicitante.has(area_id=area))
    if not estado:
        query = query.filter(Compra.estado != "CANCELADA")
    else:
        query = query.filter(Compra.estado == "CANCELADA")
    return query.order_by(Compra.fecha.asc()).all()

def procesar_contribuciones(compra_id, entidades, tabla_asociativa, atributo_saldo=None, tipo=None, estado_enum=None):
    for entidad_obj, contribucion in entidades:
        if tipo == "fondo":
            db.session.execute(
                tabla_asociativa.insert().values(
                    compra_id=compra_id,
                    fondo_id=entidad_obj.id,
                    contribucion=contribucion
                )
            )
        elif tipo == "empleado":
            db.session.execute(
                tabla_asociativa.insert().values(
                    compra_id=compra_id,
                    empleado_id=entidad_obj.id,
                    contribucion=contribucion
                )
            )
        else:
            db.session.execute(
                tabla_asociativa.insert().values(
                    compra_id=compra_id,
                    area_id=entidad_obj.id,
                    contribucion=contribucion
                )
            )
        if estado_enum == estado_compra.REALIZADA and atributo_saldo:
            setattr(entidad_obj, atributo_saldo, getattr(entidad_obj, atributo_saldo) - contribucion)
            db.session.add(entidad_obj)

def obtener_estado_enum(estado):
    if estado == "REALIZADA":
        return estado_compra.REALIZADA
    elif estado == "APROBADA":
        return estado_compra.APROBADA
    elif estado == "ESPERA":
        return estado_compra.ESPERA

def crear_compra(fecha, descripcion, proveedor, solicitante, importe, observaciones, estado, numero_factura, fondos, empleados, areas):
    estado_enum = obtener_estado_enum(estado)
    proveedor_obj = buscar_proveedor(int(proveedor))
    solicitante_obj = conseguir_empleado_de_id(int(solicitante))
    compra = Compra(
        fecha=fecha,
        descripcion=descripcion,
        proveedor=proveedor_obj,
        solicitante=solicitante_obj,
        importe=importe,
        observaciones=observaciones,
        estado=estado_enum, 
        numero_factura=numero_factura
    )
    db.session.add(compra)
    db.session.flush()
    procesar_contribuciones(compra.id, fondos, compra_fondo, atributo_saldo="saldo", tipo="fondo", estado_enum=estado_enum)
    procesar_contribuciones(compra.id, empleados, compra_empleado, atributo_saldo="saldo", tipo="empleado", estado_enum=estado_enum)
    procesar_contribuciones(compra.id, areas, compra_area, atributo_saldo="saldo", estado_enum=estado_enum)
    db.session.commit()
    return compra

def borrar_compra(compra, motivo_rechazo):
    if compra.estado == estado_compra.ESPERA:
        compra.estado = estado_compra.CANCELADA
        compra.causa_rechazo = motivo_rechazo
        db.session.commit()
    elif compra.estado == estado_compra.APROBADA:
        compra.estado = estado_compra.CANCELADA
        compra.causa_rechazo = motivo_rechazo
        db.session.execute(
            compra_fondo.delete().where(compra_fondo.c.compra_id == compra.id)
        )
        db.session.execute(
            compra_empleado.delete().where(compra_empleado.c.compra_id == compra.id)
        )
        db.session.execute(
            compra_area.delete().where(compra_area.c.compra_id == compra.id)
        )
        db.session.commit()
    return compra

def agregar_fuentes_a_compra(compra, fondos, empleados, areas):
    compra.estado = estado_compra.APROBADA
    procesar_contribuciones(compra.id, fondos, compra_fondo, tipo="fondo")
    procesar_contribuciones(compra.id, empleados, compra_empleado, tipo="empleado")
    procesar_contribuciones(compra.id, areas, compra_area)
    db.session.commit()
    return compra

def obtener_fondos(compra_id):
    return db.session.query(compra_fondo).filter_by(compra_id=compra_id).all()

def obtener_empleados(compra_id):
    return db.session.query(compra_empleado).filter_by(compra_id=compra_id).all()

def obtener_areas(compra_id):
    return db.session.query(compra_area).filter_by(compra_id=compra_id).all()

def editar_compra_espera(compra, fecha, descripcion, proveedor, solicitante, importe, observaciones, estado, numero_factura):
    estado_enum = obtener_estado_enum(estado)
    proveedor_obj = buscar_proveedor(int(proveedor))
    solicitante_obj = conseguir_empleado_de_id(int(solicitante))
    compra.fecha = fecha
    compra.descripcion = descripcion
    compra.proveedor = proveedor_obj
    compra.solicitante = solicitante_obj
    compra.importe = importe
    compra.observaciones = observaciones
    compra.estado = estado_enum
    compra.numero_factura = numero_factura
    db.session.execute(
        compra_fondo.delete().where(compra_fondo.c.compra_id == compra.id)
    )
    db.session.execute(
        compra_empleado.delete().where(compra_empleado.c.compra_id == compra.id)
    )
    db.session.execute(
        compra_area.delete().where(compra_area.c.compra_id == compra.id)
    )
    db.session.commit()
    return compra

def editar_compra_aprobada_o_realizada(compra, fecha, descripcion, proveedor, solicitante, importe, observaciones, estado, numero_factura, fondos, empleados, areas):
    estado_enum = obtener_estado_enum(estado)
    proveedor_obj = buscar_proveedor(int(proveedor))
    solicitante_obj = conseguir_empleado_de_id(int(solicitante))
    compra.fecha = fecha
    compra.descripcion = descripcion
    compra.proveedor = proveedor_obj
    compra.solicitante = solicitante_obj
    compra.importe = importe
    compra.observaciones = observaciones
    compra.estado = estado_enum
    compra.numero_factura = numero_factura
    db.session.execute(
        compra_fondo.delete().where(compra_fondo.c.compra_id == compra.id)
    )
    db.session.execute(
        compra_empleado.delete().where(compra_empleado.c.compra_id == compra.id)
    )
    db.session.execute(
        compra_area.delete().where(compra_area.c.compra_id == compra.id)
    )
    procesar_contribuciones(compra.id, fondos, compra_fondo, atributo_saldo="saldo", tipo="fondo", estado_enum=estado_enum)
    procesar_contribuciones(compra.id, empleados, compra_empleado, atributo_saldo="saldo", tipo="empleado", estado_enum=estado_enum)
    procesar_contribuciones(compra.id, areas, compra_area, atributo_saldo="saldo", estado_enum=estado_enum)
    db.session.commit()
    return compra

def realizar_compra_aprobada(compra, fondos, empleados, areas):
    compra.estado = estado_compra.REALIZADA
    db.session.execute(
        compra_fondo.delete().where(compra_fondo.c.compra_id == compra.id)
    )
    db.session.execute(
        compra_empleado.delete().where(compra_empleado.c.compra_id == compra.id)
    )
    db.session.execute(
        compra_area.delete().where(compra_area.c.compra_id == compra.id)
    )
    procesar_contribuciones(compra.id, fondos, compra_fondo, atributo_saldo="saldo", tipo="fondo", estado_enum=estado_compra.REALIZADA)
    procesar_contribuciones(compra.id, empleados, compra_empleado, atributo_saldo="saldo", tipo="empleado", estado_enum=estado_compra.REALIZADA)
    procesar_contribuciones(compra.id, areas, compra_area, atributo_saldo="saldo", estado_enum=estado_compra.REALIZADA)
    db.session.commit()
    return compra

def realizada_a_aprobada(compra):
    fondos = obtener_fondos(compra.id)
    for fondo in fondos:
        conseguir_fondo_de_id(fondo.fondo_id).saldo += fondo.contribucion
    empleados = obtener_empleados(compra.id)
    for empleado in empleados:
        conseguir_empleado_de_id(empleado.empleado_id).saldo += empleado.contribucion
    areas = obtener_areas(compra.id)
    for area in areas:
        conseguir_area_de_id(area.area_id).saldo += area.contribucion
    compra.estado = estado_compra.APROBADA
    db.session.commit()
    return compra