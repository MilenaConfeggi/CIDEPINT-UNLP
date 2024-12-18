from administracion.src.core.fondos import fondo
from administracion.src.core.ingresos import ingreso as ingresoDB
from models import distribucion as distribucionDB
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from administracion.src.web.forms.fondo_nuevo import FormularioNuevoFondo
from administracion.src.web.forms.ingreso_nuevo import FormularioNuevoIngreso
from administracion.src.web.forms.distribucion_nuevo import FormularioNuevaDistribucion
from models import legajos as legajoDB
from administracion.src.web.controllers.roles import role_required
from administracion.src.core import Area as areaDB
from administracion.src.core import Empleado as empleadoDB
#import bd
from models.base import db
from models.personal.empleado import Empleado
from models.empleado_distribucion.empleado_distribucion import Empleado_Distribucion
bp = Blueprint("contable",__name__,url_prefix="/contable")



#
from models.documentos import listar_tipos_documentos, get_tipo_documento, create_documento, find_documento, get_tipo_documento_nombre,get_documento
from models.documentos import find_estado_by_nombre
from models.documentos import create_estado
from flask import current_app as app
from datetime import datetime
from pathlib import Path
import os
from administracion.src.web.forms.documento_legajo_nuevo import UploadDocumentoForm ,DownloadForm
@bp.get("/")
@role_required('Administrador', 'Colaborador')
def index():
    return render_template("contable/home.html")
@bp.get("/fondo")
def index_fondo():
    fondos = fondo.listar_fondos()
    return render_template("contable/contable.html",fondos = fondos)

@bp.get("/fondos")
def get_crear_fondo():
    form = FormularioNuevoFondo()
    return render_template("contable/crear_fondo.html", form = form)

@bp.post("/fondos")
def crear_fondo():
    form = FormularioNuevoFondo(request.form)
    if form.validate_on_submit():
        data = request.form.to_dict()
        csrf_token = data.pop("csrf_token", None)
        if fondo.conseguir_fondo_de_id(data["titulo"]):
            flash("Ya existe un fondo con ese título", 'error')
            return render_template("contable/crear_fondo.html", form=form)
        fondo.create_fondo(**data)
        flash("Fondo creado correctamente","success")
        return redirect(url_for("contable.index"))
    else:
        # Obtener el primer campo con error
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]  # Primer error del campo
        # Mostrar el error
        flash(f"El campo {getattr(form, first_error_field).label.text} {first_error_message}", 'danger')
        return render_template("contable/crear_fondo.html", form=form)


@bp.get("/fondos/<string:fondo_id>")
def mostrar_fondo(fondo_id):
    form = FormularioNuevoIngreso()
    fond = fondo.conseguir_fondo_de_id(fondo_id)
    if not fond:
        return redirect(url_for('contable.index'))
    ingresos = ingresoDB.get_ingresos_del_fondo(fondo_id)
    #ingresos = ingresoDB.listar_ingresos()
    #print(ingresos[1].receptor_id)
    return render_template("contable/detalle_fondo.html", fondo=fond,ingresos=ingresos,form=form)
@bp.post("/ingreso/<string:fondo_id>")
def crear_ingreso(fondo_id):
    fond = fondo.conseguir_fondo_de_id(fondo_id)
    if not fond:
        return redirect(url_for('contable.index'))
    form = FormularioNuevoIngreso(request.form)
    if form.validate_on_submit():
        data = request.form.to_dict()
        data["receptor_id"] = fondo_id
        csrf_token = data.pop("csrf_token", None)
        ingresoDB.create_ingreso(**data)
        fond.saldo += float(data["monto"])
        fondo.modificar_fondo(fondo_id, saldo=fond.saldo)
        flash("Ingreso creado correctamente", "success")
        return redirect(url_for("contable.mostrar_fondo",fondo_id=fondo_id))
    else:
        # Obtener el primer campo con error
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]
    return redirect(url_for("contable.mostrar_fondo",fondo_id=fondo_id))

@bp.get("/legajos")
def get_legajos():
    legajos = legajoDB.list_legajos_all()
    forms = {}
    for legajo in legajos:
        forms[legajo.id] = UploadDocumentoForm(legajo_id=legajo.id)
    
    resultado = []

    for legajo in legajos:
        documentos = {doc.tipo_documento.nombre: doc for doc in legajo.documento}
        resultado.append({
            "id": legajo.id,
            "nro_legajo": legajo.nro_legajo,
            "cliente": legajo.cliente,
            "documentos": documentos,
        })
    form = DownloadForm()
    return render_template("contable/legajos.html",legajos = resultado, forms=forms,formDescarga = form)

@bp.get("/distribuciones/crear/<int:id>")
def get_crear_distribucion(id):
    form = FormularioNuevaDistribucion()
    empleados = empleadoDB.list_empleados()
    
    # Relación empleados-areas (simulada aquí, pero ajusta según tu base de datos)
    empleados_por_area = {}
    for empleado in empleados:
        empleados_por_area.setdefault(empleado.area_id, []).append(empleado.id)
    return render_template("contable/crear_distribucion.html", form = form,empleados_por_area=empleados_por_area, )

@bp.post("/distribuciones/crear/<int:id>")
def crear_distribucion(id):
    form = FormularioNuevaDistribucion(request.form)
    if form.validate_on_submit():
        data = request.form.to_dict()
        #Validaciones
        csrf_token = data.pop("csrf_token", None)
        data["legajo_id"] = id
        emp = data.pop("empleados_seleccionados", None)
        #Crea la distribucion
        nueva_distribucion = distribucionDB.create_distribucion(**data)
        #Sumo lo indicado al saldo de las areas
        area_ganancias = int(data["ganancias_de_id"])
        area_costos = int(data["costos_de_id"])
        porcentaje_area = float(data["porcentaje_area"]) * 0.01
        porcentaje_empleados = float(data["porcentaje_empleados"])* 0.01
        porcentaje_comisiones = float(data["porcentaje_comisiones"])* 0.01
        monto_a_distribuir = float(data["monto_a_distribuir"])
        costos = float(data["costos"])
        areaDB.sumar_saldo_area(area_costos, costos)
        monto_modificado = (monto_a_distribuir * (1 - porcentaje_comisiones))-costos
        areaDB.sumar_saldo_area(area_ganancias, (monto_modificado * porcentaje_area)*(1-porcentaje_empleados))
        # Relacion con los empleados
        empleados_ids = form.empleados_seleccionados.data
        monto_empleado = ((monto_modificado * porcentaje_area)*(porcentaje_empleados)) / len(empleados_ids)
        for empleado_id in empleados_ids:
            empleado = db.session.query(Empleado).get(empleado_id) 
            if empleado:
                empleado.saldo += monto_empleado
                empleado_distribucion = Empleado_Distribucion(
                    empleado_id=empleado.id,
                    distribucion_id=nueva_distribucion.id
                )
                db.session.add(empleado_distribucion)

                db.session.commit()
        #areaDB.sumar_saldo_area(1, monto_modificado * (1 - porcentaje_area)) Sumar a cidepint
        #Redirige a la lista de distribuciones
        flash("Distribución creada correctamente","success")
        return redirect(url_for("contable.get_legajos"))
    else:
        # Obtener el primer campo con error
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]
        return render_template("contable/crear_distribucion.html", form = form)
    
@bp.get("/distribuciones/<int:id>")
def get_distribuciones(id):
    data = distribucionDB.list_distribuciones_by_legajo(id)
    legajo = legajoDB.get_legajo(id)
    return render_template("contable/listar_distribuciones.html",distribuciones = data, legajo = legajo)

@bp.post('/upload')
def upload():
    file = request.files['file']
    tipo = request.form['tipo']
    legajo_id = request.form['legajo_id']
    
    if file.filename == '' or not file.filename.endswith('.pdf'):
        return jsonify({"error": "Por favor, selecciona un archivo PDF válido"}), 400
    td = get_tipo_documento_nombre(tipo)
    if td is None:
        return jsonify({"error": "El tipo de documento no existe"}), 400
    
    
    current_file = Path(__file__).resolve()  # Ruta absoluta del archivo actual
    project_root = current_file.parents[4]  
    DOCUMENTS_DIR = project_root / 'documentos'
    
    documentos_path = DOCUMENTS_DIR / td.nombre
    documentos_path.mkdir(parents=True, exist_ok=True)

    try:        
        file_path = documentos_path / file.filename
        data = {
            'legajo_id': legajo_id,
            'tipo_documento_id': td.id,
            'nombre_documento': None
        }
        old_file = find_documento(data)
        print(old_file)
        if old_file:
            old_documento_path = documentos_path / old_file.nombre_documento
            print(old_documento_path)
            if old_documento_path.exists():
                print(old_documento_path)
                old_documento_path.unlink()
                file.save(str(file_path))
                old_file.nombre_documento = file.filename
                db.session.commit()
                return jsonify({"message": f"Archivo guardado exitosamente en {file_path}"}), 200
            else:
                return jsonify({"error": "No se encontro el archivo"}), 404
        else:
            counter = 1
            while file_path.exists():
                file.filename = f"{Path(file.filename).stem}({counter}){Path(file.filename).suffix}"  
                file_path = documentos_path / file.filename
                counter += 1
            
            data = {
                'nombre_documento': file.filename,
                'fecha_creacion': datetime.now(),
                'estado_id': 1,
                'legajo_id': legajo_id,
                'tipo_documento_id': td.id,
            }
            if not create_documento(data):
                return jsonify({"error": "No se pudo crear el documento"}), 400

            file.save(str(file_path))
            return jsonify({"message": f"Archivo guardado exitosamente en {file_path}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@bp.get('/download/<int:documento_id>')
def download(documento_id):
     # Extraer el ID del documento desde el formulario
    archivo = get_documento(documento_id)  # Implementa esta función para buscar el documento
    if archivo is None:
        return jsonify({"error": "No se encontro el archivo"}), 404
    tipo = archivo.tipo_documento.nombre
    filename = archivo.nombre_documento

    # Ruta base de los documentos
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[4]
    documentos_path = project_root / "documentos" / tipo

    # Ruta completa del archivo
    file_path = documentos_path / filename

    # Verificar que el archivo exista
    if not file_path.exists():
        return jsonify({"error": "El archivo no existe"}), 404

    # Enviar el archivo al cliente
    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename  # Nombre que se verá al descargar
    )