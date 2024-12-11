from models.base import db
from models.archivos_admin.carpeta import Carpeta
from models.patrimonio.bien import Bien
from models.Fondo.fondo import Fondo as fondoDB
from models.personal.area import Area
from models.personal.empleado import Empleado
from models.personal.personal import User
from models.personal.ausencia import Ausencia
from sqlalchemy import MetaData
from datetime import datetime

def reset():
    """
    Resetea la base de datos
    """
    print("Eliminando base de datos en casacada")
    meta = MetaData()
    meta.reflect(bind=db.engine)
    
    # Drop foreign key constraints
    with db.engine.connect() as conn:
        for table in reversed(meta.sorted_tables):
            for fk in table.foreign_keys:
                conn.execute(db.text(f'ALTER TABLE {table.name} DROP FOREIGN KEY {fk.constraint.name}'))
    # Drop all tables
    db.drop_all()
    
    db.session.commit()
    
    print("Creando base nuevamente")
    db.create_all()
    db.session.commit()

def seed():
    default_area = Area(nombre='Default Area', saldo=0)
    db.session.add(default_area)

    bien_1 = Bien(
            titulo='Vasija',
            numero_inventario='001',
            anio=2020,
            institucion='Museo de Historia Natural',
            descripcion='Descubierta 10 anios atrás',
            area=default_area
        )
    
    bien_2 = Bien(
        titulo='Espada',
        numero_inventario='002',
        anio=1900,
        institucion='CONICET',
        descripcion='Muy buen estado',
        area=default_area
        )

    bien_3 = Bien(
        titulo='Cuchillo',
        numero_inventario='003',
        anio=2001,
        institucion='CIDEPINT',
        descripcion='Está bien feo',
        area=default_area
        )
    
    bien_4 = Bien(
        titulo='Escultura',
        numero_inventario='004',
        anio=1980,
        institucion='Museo de Arte Moderno',
        descripcion='Escultura abstracta',
        area=default_area
    )

    bien_5 = Bien(
        titulo='Pintura',
        numero_inventario='005',
        anio=1750,
        institucion='Museo del Prado',
        descripcion='Pintura renacentista',
        area=default_area
    )

    bien_6 = Bien(
        titulo='Libro',
        numero_inventario='006',
        anio=1600,
        institucion='Biblioteca Nacional',
        descripcion='Libro antiguo',
        area=default_area
    )

    bien_7 = Bien(
        titulo='Moneda',
        numero_inventario='007',
        anio=500,
        institucion='Museo Numismático',
        descripcion='Moneda de la antigua Roma',
        area=default_area
    )

    bien_8 = Bien(
        titulo='Mapa',
        numero_inventario='008',
        anio=1492,
        institucion='Archivo General de Indias',
        descripcion='Mapa del descubrimiento de América',
        area=default_area
    )

    bien_9 = Bien(
        titulo='Vasija de cerámica',
        numero_inventario='009',
        anio=300,
        institucion='Museo Arqueológico',
        descripcion='Vasija de la cultura precolombina',
        area=default_area
    )

    bien_10 = Bien(
        titulo='Joya',
        numero_inventario='010',
        anio=1800,
        institucion='Museo de Joyas',
        descripcion='Joya de la realeza',
        area=default_area
    )

    bien_11 = Bien(
        titulo='Instrumento musical',
        numero_inventario='011',
        anio=1700,
        institucion='Museo de Música',
        descripcion='Violín antiguo',
        area=default_area
    )

    bien_12 = Bien(
        titulo='Reloj',
        numero_inventario='012',
        anio=1900,
        institucion='Museo del Tiempo',
        descripcion='Reloj de bolsillo',
        area=default_area
    )

    bien_13 = Bien(
        titulo='Fotografía',
        numero_inventario='013',
        anio=1950,
        institucion='Museo de Fotografía',
        descripcion='Fotografía en blanco y negro',
        area=default_area
    )
    fondo_1 = fondoDB(
        titulo='UNLP',
        saldo=10000
    )
    db.session.add_all([bien_1,bien_2,bien_3,bien_4, bien_5, bien_6, bien_7, bien_8, bien_9, bien_10, bien_11, bien_12, bien_13,fondo_1])

    carpeta_1 = Carpeta(
        nombre="Formularios",
    )
    carpeta_2 = Carpeta(
        nombre="Informes",
    )

    carpeta_3 = Carpeta(
        nombre="Proyectos",
    )

    carpeta_4 = Carpeta(
        nombre="Contratos",
    )

    carpeta_5 = Carpeta(
        nombre="Facturas",
    )

    carpeta_6 = Carpeta(
        nombre="Recibos",
    )

    carpeta_7 = Carpeta(
        nombre="Correspondencia",
    )

    carpeta_8 = Carpeta(
        nombre="Actas",
    )

    carpeta_9 = Carpeta(
        nombre="Memorandos",
    )

    carpeta_10 = Carpeta(
        nombre="Reglamentos",
    )

    carpeta_11 = Carpeta(
        nombre="Normativas",
    )

    carpeta_12 = Carpeta(
        nombre="Manuales",
    )

    carpeta_13 = Carpeta(
        nombre="Procedimientos",
    )

    carpeta_14 = Carpeta(
        nombre="Políticas",
    )

    carpeta_15 = Carpeta(
        nombre="Planos",
    )

    carpeta_16 = Carpeta(
        nombre="Especificaciones",
    )

    carpeta_17 = Carpeta(
        nombre="Presupuestos",
    )

    db.session.add_all([carpeta_1, carpeta_2, carpeta_3, carpeta_4, carpeta_5, carpeta_6, carpeta_7, carpeta_8, carpeta_9, carpeta_10, carpeta_11, carpeta_12, carpeta_13, carpeta_14, carpeta_15, carpeta_16, carpeta_17])

    admin_user = User(
        username='admin',
        password='admin',
        habilitado=True,
        rol='Administrador'
    )
    db.session.add(admin_user)
                
    
    admin_empleado = Empleado(
        user=admin_user,
        email='admin@example.com',
        area=default_area,  # Asigna el área creada
        dni='00000000',
        nombre='Admin',
        apellido='User',
        dependencia='UNLP',
        cargo='Administrativo',
        subdivision_cargo='Ley 10430',
        telefono='123456789',
        domicilio='Admin Address',
        fecha_nacimiento=datetime.strptime('1970-01-01', '%Y-%m-%d'),
        observaciones='Usuario administrador por defecto',
    )
    db.session.add(admin_empleado)
            
    carpeta_1.usuarios_editan.append(admin_user)
    
    inhabilitado_user = User(
        username='inhabilitado',
        password='inhabilitado',
        habilitado=False,
        rol='Personal'
    )
    db.session.add(inhabilitado_user)
                
    inhabilitado_empleado = Empleado(
        user=inhabilitado_user,
        email='inhabilitado@example.com',
        area=default_area,  # Asigna el área creada
        dni='11111111',
        nombre='Inhabilitado',
        apellido='User',
        dependencia='UNLP',
        cargo='Administrativo',  # Cambiado a un valor permitido
        subdivision_cargo='Ley 10430',
        telefono='987654321',
        domicilio='Inhabilitado Address',
        fecha_nacimiento=datetime.strptime('1980-01-01', '%Y-%m-%d'),
        observaciones='Usuario inhabilitado por defecto'
    )
    db.session.add(inhabilitado_empleado)


    usuario_1 = User(
        username='rober',
        password='rober'
    )    
    
    personal_1 = Empleado(
        user=usuario_1,
        email='rober@example.com',
        area=default_area,  # Asigna el área creada
        dni='204060',
        nombre='Rober',
        apellido='Tito',
        dependencia='UNLP',
        cargo='Administrativo',
        subdivision_cargo='Ley 10430',
        telefono='123456789',
        domicilio='Admin Address',
        fecha_nacimiento=datetime.strptime('1970-01-01', '%Y-%m-%d'),
        observaciones='Usuario administrador por defecto'
    )

    usuario_2 = User(
        username='maria',
        password='maria'
    )    
    
    personal_2 = Empleado(
        user=usuario_2,
        email='maria@example.com',
        area=default_area,
        dni='204061',
        nombre='Maria',
        apellido='Lopez',
        dependencia='UNLP',
        cargo='Administrativo',
        subdivision_cargo='Ley 10430',
        telefono='123456780',
        domicilio='Maria Address',
        fecha_nacimiento=datetime.strptime('1985-02-01', '%Y-%m-%d'),
        observaciones='Usuario personal'
    )

    usuario_3 = User(
        username='juan',
        password='juan'
    )    
    
    personal_3 = Empleado(
        user=usuario_3,
        email='juan@example.com',
        area=default_area,
        dni='204062',
        nombre='Juan',
        apellido='Perez',
        dependencia='UNLP',
        cargo='Administrativo',
        subdivision_cargo='Ley 10430',
        telefono='123456781',
        domicilio='Juan Address',
        fecha_nacimiento=datetime.strptime('1990-03-01', '%Y-%m-%d'),
        observaciones='Usuario personal'
    )

    usuario_4 = User(
        username='ana',
        password='ana'
    )    
    
    personal_4 = Empleado(
        user=usuario_4,
        email='ana@example.com',
        area=default_area,
        dni='204063',
        nombre='Ana',
        apellido='Garcia',
        dependencia='UNLP',
        cargo='Administrativo',
        subdivision_cargo='Ley 10430',
        telefono='123456782',
        domicilio='Ana Address',
        fecha_nacimiento=datetime.strptime('1995-04-01', '%Y-%m-%d'),
        observaciones='Usuario personal'
    )

    usuario_5 = User(
        username='luis',
        password='luis'
    )    
    
    personal_5 = Empleado(
        user=usuario_5,
        email='luis@example.com',
        area=default_area,
        dni='204064',
        nombre='Luis',
        apellido='Martinez',
        dependencia='UNLP',
        cargo='Administrativo',
        subdivision_cargo='Ley 10430',
        telefono='123456783',
        domicilio='Luis Address',
        fecha_nacimiento=datetime.strptime('1988-05-01', '%Y-%m-%d'),
        observaciones='Usuario personal'
    )

    usuario_6 = User(
        username='laura',
        password='laura'
    )    
    
    personal_6 = Empleado(
        user=usuario_6,
        email='laura@example.com',
        area=default_area,
        dni='204065',
        nombre='Laura',
        apellido='Fernandez',
        dependencia='UNLP',
        cargo='Administrativo',
        subdivision_cargo='Ley 10430',
        telefono='123456784',
        domicilio='Laura Address',
        fecha_nacimiento=datetime.strptime('1992-06-01', '%Y-%m-%d'),
        observaciones='Usuario personal'
    )

    db.session.add_all([personal_1,usuario_1,personal_2, usuario_2, personal_3, usuario_3, personal_4, usuario_4, personal_5, usuario_5, personal_6, usuario_6])

    ausencia_1 = Ausencia(
        empleado=personal_1,
        fecha_desde=datetime.strptime('2024-12-09', '%Y-%m-%d'),
        fecha_hasta=datetime.strptime('2024-12-15', '%Y-%m-%d'),
        motivo='Vacaciones'
    )

    ausencia_2 = Ausencia(
        empleado=personal_2,
        fecha_desde=datetime.strptime('2024-11-01', '%Y-%m-%d'),
        fecha_hasta=datetime.strptime('2024-11-10', '%Y-%m-%d'),
        motivo='Enfermedad'
    )

    ausencia_3 = Ausencia(
        empleado=personal_3,
        fecha_desde=datetime.strptime('2024-10-05', '%Y-%m-%d'),
        fecha_hasta=datetime.strptime('2024-10-12', '%Y-%m-%d'),
        motivo='Capacitación'
    )

    ausencia_4 = Ausencia(
        empleado=personal_4,
        fecha_desde=datetime.strptime('2024-12-15', '%Y-%m-%d'),
        fecha_hasta=datetime.strptime('2024-12-20', '%Y-%m-%d'),
        motivo='Licencia por maternidad'
    )

    ausencia_5 = Ausencia(
        empleado=personal_5,
        fecha_desde=datetime.strptime('2024-08-01', '%Y-%m-%d'),
        fecha_hasta=datetime.strptime('2024-08-07', '%Y-%m-%d'),
        motivo='Permiso personal'
    )

    ausencia_6 = Ausencia(
        empleado=personal_6,
        fecha_desde=datetime.strptime('2024-07-10', '%Y-%m-%d'),
        fecha_hasta=datetime.strptime('2024-07-15', '%Y-%m-%d'),
        motivo='Vacaciones'
    )

    ausencia_7 = Ausencia(
        empleado=personal_1,
        fecha_desde=datetime.strptime('2024-12-01', '%Y-%m-%d'),
        fecha_hasta=datetime.strptime('2024-12-05', '%Y-%m-%d'),
        motivo='Enfermedad'
    )

    ausencia_8 = Ausencia(
        empleado=personal_2,
        fecha_desde=datetime.strptime('2024-12-20', '%Y-%m-%d'),
        fecha_hasta=datetime.strptime('2024-12-25', '%Y-%m-%d'),
        motivo='Capacitación'
    )

    db.session.add_all([ausencia_1, ausencia_2, ausencia_3, ausencia_4, ausencia_5, ausencia_6, ausencia_7, ausencia_8])

    db.session.commit()
