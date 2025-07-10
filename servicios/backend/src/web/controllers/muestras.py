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
            # Mapear los nombres de los campos enviados desde el frontend
            elem['nro_muestra'] = elem.pop('nroMuestra')
            elem['nro_grupo'] = elem.pop('nroGrupo', None)  # Opcional
            if elem['nro_grupo'] is not None and not isinstance(elem['nro_grupo'], int):
                elem['nro_grupo'] = None
            elem['fecha_ingreso'] = elem.pop('fechaIngreso')
            elem['iden_cliente'] = elem.pop('idenCliente')

            # Validar los datos con el esquema
            try:
                muestra = muestraSchema.load(elem)
            except ValidationError as err:
                return jsonify({"message": f"Error en los datos para la identificación {elem['iden_cliente']}: {err.messages}"}), 400

            # Validar que no haya muestras con la misma identificación en la base de datos
            if not servicioMuestras.validar_identificacion_cliente(muestra, id_legajo):
                return jsonify({"message": f"Ya se ingresó la identificación {elem['iden_cliente']} para este legajo"}), 400

            # Validar que no haya duplicados en el lote actual
            if not servicioMuestras.validar_entre_cargadas(muestras, muestra):
                return jsonify({"message": f"La identificación {elem['iden_cliente']} está siendo ingresada más de una vez en este lote. Modifícalo y vuelve a intentar"}), 400

            # Validar longitud de la identificación del cliente
            if not servicioMuestras.validar_longitud(muestra):
                return jsonify({"message": "La identificación del cliente no puede superar los 100 caracteres"}), 400

            # Validar que la fecha de ingreso no sea mayor a la fecha actual
            if not servicioMuestras.validar_fecha(elem['fecha_ingreso']):
                return jsonify({"message": "La fecha de ingreso no puede ser mayor a la fecha actual"}), 400

            muestras.append(muestra)

        # Crear las muestras en la base de datos
        for muestra in muestras:
            servicioMuestras.crear_muestra(muestra, id_legajo)

        return jsonify({"message": "Muestras cargadas correctamente, recargue la página para ver los cambios"}), 200

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
                'descripcion': request.form.get('descripcion', ''),  # Descripción opcional
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

        return jsonify({"message": "Fotos subidas con éxito, recargue la página para ver los cambios"}), 200
    except ValidationError as err:
        return jsonify({"message": f"Error en la validación de los datos: {err.messages}"}), 400
    except Exception as e:
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
    
@bp.delete("/eliminar_foto/<int:id_foto>")
@jwt_required()
def eliminar_foto(id_foto):
    try:
        foto = servicioMuestras.obtener_foto(id_foto)
        if not foto:
            return jsonify({"error": "Foto no encontrada"}), 404

        # Eliminar el archivo del sistema de archivos
        folder_path = os.path.join(UPLOAD_FOLDER, "muestras", str(foto.muestra.legajo_id))
        file_path = os.path.join(folder_path, foto.nombre_archivo)
        if os.path.exists(file_path):
            os.remove(file_path)

        # Eliminar la foto de la base de datos
        servicioMuestras.eliminar_foto(id_foto)
        return jsonify({"message": "Foto eliminada con éxito"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Error al eliminar la foto"}), 500

@bp.get("/ultima_muestra")
@jwt_required()
def obtener_ultima_muestra():
    ultima_muestra = servicioMuestras.obtener_ultima_muestra()
    if ultima_muestra:
        return jsonify({"ultimaMuestra": ultima_muestra}), 200
    return jsonify({}), 200

@bp.delete("/eliminar_muestra/<int:id_muestra>")
@jwt_required()
def eliminar_muestra(id_muestra):
    try:
        muestra = servicioMuestras.obtener_muestra(id_muestra)
        if not muestra:
            return jsonify({"error": "Muestra no encontrada"}), 404

        servicioMuestras.eliminar_muestra(id_muestra)
        return jsonify({"message": "Muestra eliminada con éxito"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Error al eliminar la muestra"}), 500