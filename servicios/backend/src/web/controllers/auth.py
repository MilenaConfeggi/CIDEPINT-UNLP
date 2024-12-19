from servicios.backend.src.core.config import Config
from flask import send_from_directory, jsonify, abort, Blueprint, request
from servicios.backend.src.core.services import servicioUsuario
from flask_jwt_extended import jwt_required, create_access_token
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.post("/authenticate")
def authenticate():
    try:
        # Extraer correo y contraseña del request
        mail = request.json.get("mail")
        password = request.json.get("password")
        if not mail or not password:
            return jsonify({"error": "El correo y la contraseña son obligatorios"}), 400

        # Validar el usuario
        usuario = servicioUsuario.check_user(mail, password)
        if not usuario:
            return jsonify({"error": "El usuario y la contraseña no coinciden"}), 406
        print(usuario.rol.nombre)
        if usuario.rol.nombre == "administrador":
            area = None
        else:
            area = usuario.empleado[0].area_id
        # Generar el token JWT usando el correo como identidad
        access_token = create_access_token(identity=mail)
        permisos = list(servicioUsuario.obtener_permisos(usuario))
        return jsonify({"info": "Sesión iniciada correctamente", "access_token": access_token, "permisos": permisos, "area": area}), 200
    except KeyError:
        return jsonify({"error": "Parámetros faltantes o inválidos"}), 401
    except Exception as e:
        print(e)
        return jsonify({"error": "Ha ocurrido un error"}), 500

