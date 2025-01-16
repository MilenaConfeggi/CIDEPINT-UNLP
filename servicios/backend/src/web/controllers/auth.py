from servicios.backend.src.core.config import Config
from flask import send_from_directory, jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioUsuario
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.post("/authenticate")
def authenticate():
    try:
        # Extraer correo y contraseña del request
        mail = request.json.get("mail")
        password = request.json.get("password")
        if not mail or not password:
            return jsonify({"message": "El correo y la contraseña son obligatorios"}), 400

        # Validar el usuario
        usuario = servicioUsuario.check_user(mail, password)
        if usuario is None:
            return jsonify({"message": "El usuario y la contraseña no coinciden"}), 406
        print(usuario.rol.nombre)
        if usuario.rol.nombre in ["Secretaria", "Director"]:
            area = None
        else:
            area = usuario.empleado[0].area_id
        # Generar el token JWT usando el correo como identidad
        access_token = create_access_token(identity=mail)
        permisos = list(servicioUsuario.obtener_permisos(usuario))
        cambiar_contra = usuario.cambiar_contra
        return jsonify({"message": "Sesión iniciada correctamente", "access_token": access_token, "permisos": permisos, "cambiar_contra": cambiar_contra, "area": area}), 200
    except KeyError:
        return jsonify({"message": "Parámetros faltantes o inválidos"}), 401
    except ValueError:
        return jsonify({"message": "El usuario y la contraseña no coinciden"}), 406
    except Exception as e:
        print(e)
        return jsonify({"message": "Ha ocurrido un error"}), 500

@bp.post("/cambiar_contra")
@jwt_required()
def cambiar_contra():
    try:
        password = request.json.get("password")
        passw2 = request.json.get("passw2")
        if not passw2 or not password:
            return jsonify({"message": "La contraseña es obligatoria"}), 400

        if passw2 != password:
            return jsonify({"message": "Las contraseñas no coinciden"}), 406
        
        servicioUsuario.cambiar_contra(password)
        usuario = servicioUsuario.obtener_usuario_por_mail(get_jwt_identity())
        permisos = list(servicioUsuario.obtener_permisos(usuario))

        return jsonify({"message": "Contraseña cambiada correctamente", "permisos": permisos}), 200
    except KeyError:
        return jsonify({"message": "Parámetros faltantes o inválidos"}), 401
    except Exception as e:
        print(e)
        return jsonify({"message": "Ha ocurrido un error"}), 500

@bp.post("/cambiar_contra_vieja")
@jwt_required()
def cambiar_contra_vieja():
    try:
        oldpassword = request.json.get("oldpassword")
        password = request.json.get("password")
        passw2 = request.json.get("passw2")
        if not passw2 or not password:
            return jsonify({"message": "La contraseña es obligatoria"}), 400

        if passw2 != password:
            return jsonify({"message": "Las contraseñas no coinciden"}), 406
        
        usuario = servicioUsuario.check_user(get_jwt_identity(), oldpassword)
        
        servicioUsuario.cambiar_contra(password)

        return jsonify({"message": "Contraseña cambiada correctamente"}), 200
    except KeyError:
        return jsonify({"message": "Parámetros faltantes o inválidos"}), 401
    except ValueError:
        return jsonify({"message": "La contraseña actual es incorrecta"}), 406
    except Exception as e:
        print(e)
        return jsonify({"message": "Ha ocurrido un error"}), 500
