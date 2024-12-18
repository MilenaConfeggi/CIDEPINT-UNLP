from models.compras.proveedor import Proveedor
from models.base import db

def listar_proveedores():
    return Proveedor.query.filter(Proveedor.activo == True).all()

def filtrar_proveedores(razon_social, contacto, page, per_page):
    query = Proveedor.query.filter(Proveedor.activo == True)

    if razon_social:
        query = query.filter(Proveedor.razon_social.ilike(f"{razon_social}%"))
    if contacto:
        query = query.filter(Proveedor.contacto.ilike(f"{contacto}%"))
    
    return query.order_by(Proveedor.razon_social.asc()).paginate(page=page,per_page=per_page,error_out=False)

def chequeo_razon_social_existente(razon_social):
    return Proveedor.query.filter(Proveedor.razon_social == razon_social, Proveedor.activo == True).first()

def crear_proveedor(razon_social, contacto):
    proveedor = Proveedor(razon_social=razon_social, contacto=contacto)
    db.session.add(proveedor)
    db.session.commit()
    return proveedor

def actualizar_proveedor(id_proveedor, razon_social, contacto):
    proveedor = Proveedor.query.get(id_proveedor)
    if proveedor:
        proveedor.razon_social = razon_social
        proveedor.contacto = contacto
        db.session.commit()
    return proveedor

def buscar_proveedor(id):
    return Proveedor.query.filter(Proveedor.id == id, Proveedor.activo == True).first()

def borrar_proveedor(id, mensaje, estado):
    proveedor = Proveedor.query.get(id)
    if proveedor:
        proveedor.activo = False
        db.session.commit()
        mensaje = "Proveedor eliminado exitosamente"
        estado = "success"
    else:
        mensaje = "Proveedor no encontrado"
        estado = "danger"
    return mensaje, estado