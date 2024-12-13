from datetime import datetime
from servicios.backend.src.core.services.servicioUsuario import crear_usuario, crear_rol, crear_permiso, asignar_permiso
from models.usuarios.rol import Rol
from models.usuarios.permiso import Permiso
from models.personal.empleado import Empleado
from models.personal.personal import User
from models.personal.area import Area
from models.base import db


def seeds_usuarios():
    seed_usuarios()


def seed_usuarios():
    rol_trabajador = crear_rol({"nombre": "trabajador"})
    db.session.add(rol_trabajador)
    rol_jefe_de_area = crear_rol({"nombre": "jefe_de_area"})
    db.session.add(rol_jefe_de_area)
    rol_secretaria = crear_rol({"nombre": "secretaria"})
    db.session.add(rol_secretaria)
    rol_director = crear_rol({"nombre": "director"})
    db.session.add(rol_director)
    db.session.commit()

    default_area = Area(nombre='Area 2fault', saldo=0)

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
        observaciones='Usuario administrador por defecto',
        habilitado=True,
        rol='Personal'
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
        observaciones='Usuario personal',
        habilitado=True,
        rol='Personal'
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
        observaciones='Usuario personal',
        habilitado=True,
        rol='Personal'
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
        observaciones='Usuario personal',
        habilitado=True,
        rol='Personal'
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
        observaciones='Usuario personal',
        habilitado=True,
        rol='Personal'
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
        observaciones='Usuario personal',
        habilitado=True,
        rol='Personal'
    )

    db.session.add(usuario_1)
    db.session.add(usuario_2)
    db.session.add(usuario_3)
    db.session.add(usuario_4)
    db.session.add(usuario_5)
    db.session.add(usuario_6)

    db.session.add(personal_1)
    db.session.add(personal_2)
    db.session.add(personal_3)
    db.session.add(personal_4)
    db.session.add(personal_5)
    db.session.add(personal_6)

    usuario1 = crear_usuario(
        {
            "mail": "pepito@example.com",
            "contra": "123",
            "rol": rol_trabajador,
            "empleado": personal_1,
        }
    )
    usuario2 = crear_usuario(
        {
            "mail": "moniquita@example.com",
            "contra": "321",
            "rol": rol_jefe_de_area,
            "empleado": personal_2,
        }
    )
    usuario3 = crear_usuario(
        {
            "mail": "director@example.com",
            "contra": "soyadmin",
            "rol": rol_director,
            "empleado": personal_3,
        }
    )
    usuario4 = crear_usuario(
        {
            "mail": "secretaria@example.com",
            "contra": "soysecretaria",
            "rol": rol_secretaria,
            "empleado": personal_4,
        }
    )
    db.session.add(usuario1)
    db.session.add(usuario2)
    db.session.add(usuario3)
    db.session.add(usuario4)

    todosLosPermisos = [ #Acá van todos los permisos a insertar (todos los posibles permisos que hay en el sistema)
        "listar_usuarios", #Por favor, ponerle el mismo nombre que el nombre del método del controlador
        "borrar_usuario",
        "listar_stans",
        "cargar_stan",
        "cargar_muestra",
        "listar_muestras_identificadas",
        "terminar_muestra",
        "cargar_fotos",
        "listar_fotos",
        "descargar_fotos",
        "enviar_fotos",
    ]
    PERMISSIONS = { #Acá van los permisos que tiene cada rol
        "director": [ #Tienen que ser declarados previamente en todosLosPermisos
            "listar_usuarios",
            "borrar_usuario",
            "listar_stans",
            "cargar_stan",
            "cargar_muestra",
            "listar_muestras_identificadas",
            "terminar_muestra",
            "cargar_fotos",
            "listar_fotos",
            "descargar_fotos",
            "enviar_fotos",
        ],
        "secretaria": [
            "listar_usuarios",
            "borrar_usuario",
            "listar_stans",
            "cargar_stan",
            "cargar_muestra",
            "listar_muestras_identificadas",
            "terminar_muestra",
            "cargar_fotos",
            "listar_fotos",
            "descargar_fotos",
            "enviar_fotos",
        ],
        "jefe_de_area": [
            "listar_muestras_identificadas",
            "cargar_fotos",
            "listar_fotos",
        ],
        "trabajador": [
            "listar_muestras_identificadas",
            "cargar_fotos",
            "listar_fotos",
        ],
    }

    for per in todosLosPermisos:
        permission = crear_permiso(
            {
                "nombre": per,
            }
        )

    def find_permission_by_name(permiso):
        return Permiso.query.filter_by(nombre=permiso).first()

    def find_role_by_name(rol):
        return Rol.query.filter_by(nombre=rol).first()

    for rol in PERMISSIONS:
        for per in PERMISSIONS[rol]:
            asignar_permiso(
                {
                    "rol": (find_role_by_name(rol)),
                    "permiso": (find_permission_by_name(per))
                }
            )


    db.session.commit()


