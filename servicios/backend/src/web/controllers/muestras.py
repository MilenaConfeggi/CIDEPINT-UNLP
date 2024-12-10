from servicios.backend.src.core.services import servicioMuestras, servicioMail
from flask import Blueprint, jsonify, abort, request, send_file, send_from_directory
from servicios.backend.src.web.schemas.muestras import muestrasSchema, muestraSchema, fotosSchema, fotoSchema
import os
from werkzeug.utils import secure_filename
from marshmallow import ValidationError

UPLOAD_FOLDER = os.path.abspath("documentos")

bp = Blueprint('muestras', __name__, url_prefix='/muestras')

@bp.get("/<int:id_legajo>")
def listar_muestras_identificadas(id_legajo):
    mails = servicioMuestras.listar_muestras(id_legajo)
    data = muestrasSchema.dump(mails, many=True)
    return jsonify(data), 200

@bp.post("/subir_muestras/<int:id_legajo>")
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
def terminar_muestra(id_muestra):
    muestra = servicioMuestras.terminar_muestra(id_muestra)
    return jsonify({"message": "La muestra se terminó con exito"}), 200


@bp.post("/subir_fotos/<int:legajo_id>")
def cargar_fotos(legajo_id):
    if 'archivo' not in request.files:
        return jsonify({"error": "Debes seleccionar un archivo"}), 400

    archivo = request.files['archivo']
    muestra_id = request.form.get('muestra_id')
    fecha = request.form.get('fecha')

    if not archivo or archivo.filename == '':
        return jsonify({"error": "Por favor seleccione un archivo"}), 400

    if not muestra_id or not fecha:
        return jsonify({"error": "Muestra y fecha son requeridos"}), 400

    try:
        muestra_id = int(muestra_id)
        filename = secure_filename(archivo.filename).replace(" ", "_")  # Reemplazar espacios con guion bajo
        foto_data = {
            'nombre_archivo': filename,
            'fecha': fecha,
            'muestra_id': muestra_id
        }
        try:
            foto = fotoSchema.load(foto_data)
        except ValidationError as err:
                return jsonify({"message": f"Error en la fecha  {fecha}"}), 400
        if( not servicioMuestras.validar_fecha(foto.get('fecha'))):
            return jsonify({"message": "La fecha de la foto no puede ser mayor a la fecha actual"}), 400
        servicioMuestras.crear_foto(foto, muestra_id)
        
        # Guardar el archivo en el servidor
        folder_path = os.path.join(UPLOAD_FOLDER, "muestras", str(muestra_id))
        os.makedirs(folder_path, exist_ok=True)
        archivo.save(os.path.join(folder_path, filename))

        return jsonify({"message": "Fotos subidas con éxito"}), 200
    except ValidationError as err:
        print(err.messages)  # Imprime los mensajes de error de validación
        return jsonify({"message": f"Error en la validación de los datos: {err.messages}"}), 400
    except Exception as e:
        print(e)  # Imprime el error para depuración
        return jsonify({"message": "Ha ocurrido un error inesperado"}), 500
  

@bp.get("/fotos/<int:id_muestra>")
def listar_fotos(id_muestra):
    fotos = servicioMuestras.listar_fotos(id_muestra)
    data = fotosSchema.dump(fotos, many=True)
    return jsonify(data), 200

@bp.get("/imagenes/<int:id_muestra>/<filename>")
def obtener_imagen(id_muestra, filename):
    folder_path = os.path.normpath(os.path.join(UPLOAD_FOLDER, "muestras", str(id_muestra)))
    file_path = os.path.normpath(os.path.join(folder_path, filename))
    if not os.path.exists(file_path):
        abort(404, description="Resource not found")
    return send_from_directory(folder_path, filename)

@bp.get("/fotos_por_legajo/<int:id_legajo>")
def listar_fotos_por_legajo(id_legajo):
    fotos = servicioMuestras.listar_fotos_por_legajo(id_legajo)
    data = fotosSchema.dump(fotos, many=True)
    return jsonify(data), 200

@bp.get("/fotos_por_fecha/<int:id_legajo>/<fecha>")
def listar_fotos_por_fecha(id_legajo, fecha):
    fotos = servicioMuestras.listar_fotos_por_fecha(id_legajo, fecha)
    data = fotosSchema.dump(fotos, many=True)
    return jsonify(data), 200

@bp.get("/descargar_fotos/<int:id_muestra>/<filename>")
def descargar_foto(id_muestra, filename):
    folder_path = os.path.normpath(os.path.join(UPLOAD_FOLDER, "muestras", str(id_muestra)))
    file_path = os.path.normpath(os.path.join(folder_path, filename))
    if not os.path.exists(file_path):
        abort(404, description="Resource not found")
    return send_file(file_path, as_attachment=True)

@bp.get("/")
def listar_muestras():
    muestras = servicioMuestras.listar_todas()
    data = muestrasSchema.dump(muestras)
    return jsonify(data), 200