from datetime import datetime
from servicios.backend.src.core.services.servicioUsuario import crear_usuario, crear_rol, crear_permiso, asignar_permiso
from models.usuarios.rol import Rol
from models.usuarios.permiso import Permiso
from models.base import db
from web import bcrypt




def seeds_usuarios():
    seed_usuarios()


def seed_usuarios():
    rol_trabajador = crear_rol({"nombre": "trabajador"})
    db.session.add(rol_trabajador)
    rol_jefe_de_area = crear_rol({"nombre": "jefe_de_area"})
    db.session.add(rol_jefe_de_area)
    rol_administrador = crear_rol({"nombre": "administrador"})
    db.session.add(rol_administrador)
    db.session.commit()

    usuario1 = crear_usuario(
        {
            "mail": "pepito@example.com",
            "contra": bcrypt.generate_password_hash("123".encode("utf-8")),
            "rol": rol_trabajador,
        }
    )
    usuario2 = crear_usuario(
        {
            "mail": "moniquita@example.com",
            "contra": bcrypt.generate_password_hash("321".encode("utf-8")),
            "rol": rol_jefe_de_area,
        }
    )
    usuario3 = crear_usuario(
        {
            "mail": "admin@example.com",
            "contra": bcrypt.generate_password_hash("soyadmin".encode("utf-8")),
            "rol": rol_administrador,
        }
    )
    db.session.add(usuario1)
    db.session.add(usuario2)
    db.session.add(usuario3)

    todosLosPermisos = [ #Acá van todos los permisos a insertar (todos los posibles permisos que hay en el sistema)
        "listar_usuarios", #Por favor, ponerle el mismo nombre que el nombre del método del controlador
        "borrar_usuario",
        "listar_stans",
        "cargar_stan",
    ]
    PERMISSIONS = { #Acá van los permisos que tiene cada rol
        "administrador": [ #Tienen que ser declarados previamente en todosLosPermisos
            "listar_usuarios",
            "borrar_usuario",
            "listar_stans",
            "cargar_stan"
        ],
        "jefe_de_area": [
        ],
        "trabajador": [
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


