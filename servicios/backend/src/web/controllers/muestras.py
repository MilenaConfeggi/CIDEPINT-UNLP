from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from servicios.backend.src.core.services import servicioMuestras, servicioUsuario
from flask import Blueprint, jsonify, abort, request, send_file, send_from_directory
from servicios.backend.src.web.schemas.muestras import muestrasSchema, muestraSchema, fotosSchema, fotoSchema
import os
from werkzeug.utils import secure_filename
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from servicios.backend.src.web.helpers.auth import is_authenticated, check_permission
import smtplib
import zipfile
from io import BytesIO
from servicios.backend.src.core.config import config
from models.legajos import find_mail_legajo
UPLOAD_FOLDER = os.path.abspath("documentos")

bp = Blueprint('muestras', __name__, url_prefix='/muestras')

@bp.get("/<int:id_legajo>")
@jwt_required()
def listar_muestras_identificadas(id_legajo):
    if not check_permission("listar_muestras_identificadas"):
        return jsonify({"Error": "No tiene permiso para acceder a este recurso"}), 403
    muestras = servicioMuestras.listar_muestras(id_legajo)
    if not muestras:
        print("No se encontraron muestras para el legajo proporcionado")
        return jsonify({"Error": "No se encontraron muestras para el legajo proporcionado"}), 404
    data = muestrasSchema.dump(muestras, many=True)
    return jsonify(data), 200

@bp.post("/subir_muestras/<int:id_legajo>")
@jwt_required()
def cargar_muestra(id_legajo):
    try:
        data = request.get_json()
        muestras = []
        for elem in data:
            elem['fecha_ingreso'] = elem.pop('fechaIngreso')
            elem['iden_cliente'] = elem.pop('idenCliente')
            try:
                muestra = muestraSchema.load(elem)
            except ValidationError as err:
                return jsonify({"message": f"Error en la fecha para la identificación {elem['iden_cliente']}"}), 400
            muestra = muestraSchema.load(elem)
            #valido que no haya muestras cargadas previamente con la misma identificacion
            if not servicioMuestras.validar_identificacion_cliente(muestra, id_legajo):
                return jsonify({"message": f"Ya se ingresó la identificación {elem['iden_cliente']} para este legajo"}), 400
            #valido que entre las que se cargar al mismo tiempo no tengan la misma identificacion
            if not servicioMuestras.validar_entre_cargadas(muestras, muestra):
                return jsonify({"message": f"La identificación {elem['iden_cliente']} está siendo ingresada más de una vez en este lote. Modificalo y vuelve a intentar"}), 400
            if not servicioMuestras.validar_longitud(muestra):
                return jsonify({"message": "La identificación del cliente no puede superar los 100 caracteres"}), 400
            print("fecha ingreso", elem['fecha_ingreso'])
            if not servicioMuestras.validar_fecha(elem['fecha_ingreso']):
                return jsonify({"message": "La fecha de ingreso no puede ser mayor a la fecha actual"}), 400
            muestras.append(muestra)
        for muestra in muestras:
            muestra = servicioMuestras.crear_muestra(muestra, id_legajo)

        return jsonify({"message": "Muestras cargadas correctamente"}), 200
    except ValidationError as e:
        return jsonify({"message": "Ha ocurrido un error inesperado, revise que muestras se han cargado antes de volver a intentarlo"}), 400
    except Exception as e:
        return jsonify({"message": "Ha ocurrido un error inesperado, revise que muestras se han cargado antes de volver a intentarlo"}), 500

@bp.post("/terminar_muestra/<int:id_muestra>")
@jwt_required()
def terminar_muestra(id_muestra):
    muestra = servicioMuestras.terminar_muestra(id_muestra)
    return jsonify({"message": "La muestra se terminó con exito"}), 200


@bp.post("/subir_fotos/<int:legajo_id>")
@jwt_required()
def cargar_fotos(legajo_id):
    if 'archivos' not in request.files:
        return jsonify({"error": "Debes seleccionar al menos un archivo"}), 400

    archivos = request.files.getlist('archivos')
    fecha = request.form.get('fecha')

    if not archivos or any(archivo.filename == '' for archivo in archivos):
        return jsonify({"error": "Por favor selecciona archivos válidos"}), 400

    if not fecha:
        return jsonify({"error": "La fecha es requerida"}), 400

    try:
        for archivo in archivos:
            filename = secure_filename(archivo.filename).replace(" ", "_")  # Reemplazar espacios con guion bajo
            foto_data = {
                'nombre_archivo': filename,
                'fecha': fecha,
                'legajo_id': legajo_id,  # Añadir legajo_id
                'muestra_id': None  # No se relaciona con una muestra
            }
            try:
                foto = fotoSchema.load(foto_data)
            except ValidationError as err:
                return jsonify({"message": f"Error en la fecha {fecha}"}), 400
            if not servicioMuestras.validar_fecha(foto.get('fecha')):
                return jsonify({"message": "La fecha de la foto no puede ser mayor a la fecha actual"}), 400
            if servicioMuestras.hay_muestra_legajo(legajo_id) == None:
                return jsonify({"message": "Aun no hay muestras identificadas para este legajo"}), 404
            servicioMuestras.crear_foto(foto, servicioMuestras.hay_muestra_legajo(legajo_id).id)
            
            # Guardar el archivo en el servidor
            folder_path = os.path.join(UPLOAD_FOLDER, "muestras", str(legajo_id))
            os.makedirs(folder_path, exist_ok=True)
            archivo.save(os.path.join(folder_path, filename))

        return jsonify({"message": "Fotos subidas con éxito"}), 200
    except ValidationError as err:
        print(err.messages)  # Imprime los mensajes de error de validación
        return jsonify({"message": f"Error en la validación de los datos: {err.messages}"}), 400
    except Exception as e:
        print(e)  # Imprime el error para depuración
        return jsonify({"message": "Ha ocurrido un error inesperado"}), 500
  

@bp.get("/imagenes/<int:id_legajo>/<filename>")
def obtener_imagen(id_legajo, filename):
    folder_path = os.path.normpath(os.path.join(UPLOAD_FOLDER, "muestras", str(id_legajo)))
    file_path = os.path.normpath(os.path.join(folder_path, filename))
    if not os.path.exists(file_path):
        abort(404, description="Resource not found")
    return send_from_directory(folder_path, filename)

@bp.get("/fotos_por_legajo/<int:id_legajo>")
@jwt_required()
def listar_fotos_por_legajo(id_legajo):
    fotos = servicioMuestras.listar_fotos_por_legajo(id_legajo)
    print(fotos)
    data = fotosSchema.dump(fotos, many=True)
    return jsonify(data), 200

@bp.get("/fotos_por_fecha/<int:id_legajo>/<fecha>")
@jwt_required()
def listar_fotos_por_fecha(id_legajo, fecha):
    fotos = servicioMuestras.listar_fotos_por_fecha(id_legajo, fecha)
    data = fotosSchema.dump(fotos, many=True)
    return jsonify(data), 200

@bp.get("/descargar_fotos/<int:id_muestra>/<filename>")
@jwt_required()
def descargar_foto(id_muestra, filename):
    folder_path = os.path.normpath(os.path.join(UPLOAD_FOLDER, "muestras", str(id_muestra)))
    file_path = os.path.normpath(os.path.join(folder_path, filename))
    if not os.path.exists(file_path):
        abort(404, description="Resource not found")
    return send_file(file_path, as_attachment=True)

@bp.get("/")
def listar_muestras():
    muestras = servicioMuestras.listar_todas()
    if muestras:
        data = muestrasSchema.dump(muestras)
        return jsonify(data), 200
    else:
        return jsonify({"message": "No se encontraron muestras"}), 404

@bp.post("/enviar_mail/<int:id_legajo>/<fecha>")
@jwt_required()
def enviar_mail(id_legajo, fecha):
    fotos = servicioMuestras.listar_fotos_por_fecha(id_legajo, fecha)
    if not fotos:
        return jsonify({"error": "No se encontraron fotos para la fecha proporcionada"}), 404

    # Crear un archivo ZIP en memoria
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for foto in fotos:
            file_path = os.path.join(UPLOAD_FOLDER, "muestras", str(foto.muestra_id), foto.nombre_archivo)
            zip_file.write(file_path, os.path.basename(file_path))

    zip_buffer.seek(0)

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(config["development"].MAIL_USER, config["development"].MAIL_PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = config["development"].MAIL_USER
        correo = find_mail_legajo(id_legajo)
        msg["To"] = correo
        msg["Subject"] = "Fotos de muestras"

        body = "Adjunto encontrarás las fotos de las muestras correspondientes a la fecha proporcionada."
        msg.attach(MIMEText(body, 'plain'))

        # Adjuntar el archivo ZIP
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(zip_buffer.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="fotos_muestras.zip"')
        msg.attach(part)

        servidor.sendmail(config["development"].MAIL_USER, correo, msg.as_string())
        servidor.quit()
        return jsonify({"message": "Correo enviado correctamente"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "No se pudo enviar el correo"}), 500

@bp.get("/permiso/<int:id_legajo>")
@jwt_required()  
def permiso(id_legajo):
    usuario = servicioUsuario.obtener_usuario_por_mail(get_jwt_identity())
    if servicioUsuario.es_director(usuario) or servicioUsuario.es_secretaria(usuario):
        return jsonify(""), 200
    if not servicioMuestras.tiene_permiso(id_legajo, usuario.mail):
        return jsonify({"message": "No tiene permiso para acceder a esta muestra"}), 403
    return jsonify(""), 200
    