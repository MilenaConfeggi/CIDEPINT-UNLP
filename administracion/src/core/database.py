from models import db
from models.patrimonio.bien import Bien
from models.compras.proveedor import Proveedor
from models.compras.compra import Compra, estado_compra
from datetime import datetime

def reset():
    """
    Resetea la base de datos
    """

    db.drop_all()
    db.create_all()

def seed():
    bien_1 = Bien(
            titulo='Vasija',
            numero_inventario='001',
            anio=2020,
            institucion='Museo de Historia Natural',
            descripcion='Descubierta 10 anios atrás',
        )
    
    bien_2 = Bien(
        titulo='Espada',
        numero_inventario='002',
        anio=1900,
        institucion='CONICET',
        descripcion='Muy buen estado',
        )

    bien_3 = Bien(
        titulo='Cuchillo',
        numero_inventario='003',
        anio=2001,
        institucion='CIDEPINT',
        descripcion='Está bien feo',
        )
    
    bien_4 = Bien(
        titulo='Escultura',
        numero_inventario='004',
        anio=1980,
        institucion='Museo de Arte Moderno',
        descripcion='Escultura abstracta',
    )

    bien_5 = Bien(
        titulo='Pintura',
        numero_inventario='005',
        anio=1750,
        institucion='Museo del Prado',
        descripcion='Pintura renacentista',
    )

    bien_6 = Bien(
        titulo='Libro',
        numero_inventario='006',
        anio=1600,
        institucion='Biblioteca Nacional',
        descripcion='Libro antiguo',
    )

    bien_7 = Bien(
        titulo='Moneda',
        numero_inventario='007',
        anio=500,
        institucion='Museo Numismático',
        descripcion='Moneda de la antigua Roma',
    )

    bien_8 = Bien(
        titulo='Mapa',
        numero_inventario='008',
        anio=1492,
        institucion='Archivo General de Indias',
        descripcion='Mapa del descubrimiento de América',
    )

    bien_9 = Bien(
        titulo='Vasija de cerámica',
        numero_inventario='009',
        anio=300,
        institucion='Museo Arqueológico',
        descripcion='Vasija de la cultura precolombina',
    )

    bien_10 = Bien(
        titulo='Joya',
        numero_inventario='010',
        anio=1800,
        institucion='Museo de Joyas',
        descripcion='Joya de la realeza',
    )

    bien_11 = Bien(
        titulo='Instrumento musical',
        numero_inventario='011',
        anio=1700,
        institucion='Museo de Música',
        descripcion='Violín antiguo',
    )

    bien_12 = Bien(
        titulo='Reloj',
        numero_inventario='012',
        anio=1900,
        institucion='Museo del Tiempo',
        descripcion='Reloj de bolsillo',
    )

    bien_13 = Bien(
        titulo='Fotografía',
        numero_inventario='013',
        anio=1950,
        institucion='Museo de Fotografía',
        descripcion='Fotografía en blanco y negro',
    )

    proveedor_1 = Proveedor(
        razon_social = "mio",
        contacto = "123"
    )

    db.session.add(proveedor_1)

    compra_1 = Compra(
        fecha = datetime.now(),
        numero_factura = "jamon",
        importe = 89,
        descripcion = "es un jamon",
        estado = estado_compra.PENDIENTE,      
        proveedor = proveedor_1
    )

    db.session.add(compra_1)

    db.session.add_all([bien_1,bien_2,bien_3,bien_4, bien_5, bien_6, bien_7, bien_8, bien_9, bien_10, bien_11, bien_12, bien_13])
    db.session.commit()
