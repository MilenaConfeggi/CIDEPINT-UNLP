from models.compras.compra import Compra, estado_compra
from models.compras.compra_fondo import compra_fondo
from models.compras.compra_empleado import compra_empleado
from models.compras.compra_area import compra_area
from sqlalchemy.orm import joinedload
from models.base import db
from administracion.src.core.proveedores.proveedor import buscar_proveedor
from administracion.src.core.servicios.personal import conseguir_empleado_de_id

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

def crear_compra(fecha, descripcion, proveedor, solicitante, importe, observaciones, estado, numero_factura, fondos, empleados, areas):
    if estado == "REALIZADA":
        estado_enum = estado_compra.REALIZADA
    elif estado == "APROBADA":
        estado_enum = estado_compra.APROBADA
    elif estado == "ESPERA":
        estado_enum = estado_compra.ESPERA
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
    for fondo_obj, contribucion in fondos:
        db.session.execute(
            compra_fondo.insert().values(
                compra_id=compra.id,
                fondo_titulo=fondo_obj.titulo,
                contribucion=contribucion,
            )
        )
        if estado_enum == estado_compra.REALIZADA:
            fondo_obj.saldo -= contribucion
            db.session.add(fondo_obj)
    for empleado_obj, contribucion in empleados:
        db.session.execute(
            compra_empleado.insert().values(
                compra_id=compra.id,
                empleado_id=empleado_obj.id,
                contribucion=contribucion,
            )
        )
        if estado_enum == estado_compra.REALIZADA:
            empleado_obj.saldo -= contribucion
            db.session.add(empleado_obj)
    for area_obj, contribucion in areas:
        db.session.execute(
            compra_area.insert().values(
                compra_id=compra.id,
                area_id=area_obj.id,
                contribucion=contribucion,
            )
        )
        if estado_enum == estado_compra.REALIZADA:
            area_obj.saldo -= contribucion
            db.session.add(area_obj)
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
    for fondo_obj, contribucion in fondos:
        db.session.execute(
            compra_fondo.insert().values(
                compra_id=compra.id,
                fondo_titulo=fondo_obj.titulo,
                contribucion=contribucion,
            )
        )
    for empleado_obj, contribucion in empleados:
        db.session.execute(
            compra_empleado.insert().values(
                compra_id=compra.id,
                empleado_id=empleado_obj.id,
                contribucion=contribucion,
            )
        )
    for area_obj, contribucion in areas:
        db.session.execute(
            compra_area.insert().values(
                compra_id=compra.id,
                area_id=area_obj.id,
                contribucion=contribucion,
            )
        )
    db.session.commit()
    return compra

def obtener_fondos(compra_id):
    return db.session.query(compra_fondo).filter_by(compra_id=compra_id).all()

def obtener_empleados(compra_id):
    return db.session.query(compra_empleado).filter_by(compra_id=compra_id).all()

def obtener_areas(compra_id):
    return db.session.query(compra_area).filter_by(compra_id=compra_id).all()

def editar_compra_espera(compra, fecha, descripcion, proveedor, solicitante, importe, observaciones, estado, numero_factura):
    if estado == "REALIZADA":
        estado_enum = estado_compra.REALIZADA
    elif estado == "APROBADA":
        estado_enum = estado_compra.APROBADA
    elif estado == "ESPERA":
        estado_enum = estado_compra.ESPERA
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
    if estado == "REALIZADA":
        estado_enum = estado_compra.REALIZADA
    elif estado == "APROBADA":
        estado_enum = estado_compra.APROBADA
    elif estado == "ESPERA":
        estado_enum = estado_compra.ESPERA
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
    for fondo_obj, contribucion in fondos:
        db.session.execute(
            compra_fondo.insert().values(
                compra_id=compra.id,
                fondo_titulo=fondo_obj.titulo,
                contribucion=contribucion,
            )
        )
        if estado_enum == estado_compra.REALIZADA:
            fondo_obj.saldo -= contribucion
            db.session.add(fondo_obj)
    for empleado_obj, contribucion in empleados:
        db.session.execute(
            compra_empleado.insert().values(
                compra_id=compra.id,
                empleado_id=empleado_obj.id,
                contribucion=contribucion,
            )
        )
        if estado_enum == estado_compra.REALIZADA:
            empleado_obj.saldo -= contribucion
            db.session.add(empleado_obj)
    for area_obj, contribucion in areas:
        db.session.execute(
            compra_area.insert().values(
                compra_id=compra.id,
                area_id=area_obj.id,
                contribucion=contribucion,
            )
        )
        if estado_enum == estado_compra.REALIZADA:
            area_obj.saldo -= contribucion
            db.session.add(area_obj)
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
    for fondo_obj, contribucion in fondos:
        db.session.execute(
            compra_fondo.insert().values(
                compra_id=compra.id,
                fondo_titulo=fondo_obj.titulo,
                contribucion=contribucion,
            )
        )
        fondo_obj.saldo -= contribucion
        db.session.add(fondo_obj)
    for empleado_obj, contribucion in empleados:
        db.session.execute(
            compra_empleado.insert().values(
                compra_id=compra.id,
                empleado_id=empleado_obj.id,
                contribucion=contribucion,
            )
        )
        empleado_obj.saldo -= contribucion
        db.session.add(empleado_obj)
    for area_obj, contribucion in areas:
        db.session.execute(
            compra_area.insert().values(
                compra_id=compra.id,
                area_id=area_obj.id,
                contribucion=contribucion,
            )
        )
        area_obj.saldo -= contribucion
        db.session.add(area_obj)
    db.session.commit()
    return compra