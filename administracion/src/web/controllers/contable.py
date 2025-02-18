from administracion.src.core.fondos import fondo
from administracion.src.core.ingresos import ingreso as ingresoDB
from administracion.src.core.servicios import archivos_admin as archivos_adminDB
from models import distribucion as distribucionDB
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file, send_from_directory
from flask_login import current_user
from administracion.src.web.forms.fondo_nuevo import FormularioNuevoFondo
from administracion.src.web.forms.ingreso_nuevo import FormularioNuevoIngreso
from administracion.src.web.forms.distribucion_nuevo import FormularioNuevaDistribucion
from models import legajos as legajoDB
from models.legajos.legajo import Legajo
from administracion.src.web.controllers.roles import role_required
from administracion.src.core import Area as areaDB
from administracion.src.core import Empleado as empleadoDB
#import bd
from models.base import db
from models.personal.empleado import Empleado
from models.empleado_distribucion.empleado_distribucion import Empleado_Distribucion
from decimal import Decimal
from models.documentos import listar_tipos_documentos, get_tipo_documento, create_documento, find_documento, get_tipo_documento_nombre,get_documento
from models.documentos import find_estado_by_nombre
from models.documentos import create_estado
from flask import current_app as app
from datetime import datetime
from pathlib import Path
import os
from administracion.src.web.forms.documento_legajo_nuevo import UploadDocumentoForm ,DownloadForm ,DeleteForm

bp = Blueprint("contable",__name__,url_prefix="/contable")

@bp.get("/")
@role_required('Administrador', 'Colaborador')
def index():
    return render_template("contable/home.html")

@bp.get("/fondo")
@role_required('Administrador', 'Colaborador')
def index_fondo():
    page = request.args.get("page", 1, type=int)
    per_page = 10

    fondos = fondo.filtrar_fondos(page=page, per_page=per_page)
   # fondos = [f for f in fondos if not f.borrado]
    return render_template("contable/contable.html",fondos = fondos)

@bp.get("/fondos")
@role_required('Administrador', 'Colaborador')
def get_crear_fondo():
    form = FormularioNuevoFondo()
    return render_template("contable/crear_fondo.html", form = form)

@bp.post("/fondos")
@role_required('Administrador', 'Colaborador')
def crear_fondo():
    form = FormularioNuevoFondo(request.form)
    if form.validate_on_submit():
        data = request.form.to_dict()
        csrf_token = data.pop("csrf_token", None)
        if fondo.conseguir_fondo_por_nombre(data["titulo"]):
            flash("Ya existe un fondo con ese título", 'error')
            return render_template("contable/crear_fondo.html", form=form)
        #Crear carpeta
        if archivos_adminDB.chequear_nombre_carpeta_existente(data["titulo"]):
            flash("Ya existe una carpeta con ese título", 'error')
            return render_template("contable/crear_fondo.html", form=form)
        x = fondo.create_fondo(**data)
        carpeta = archivos_adminDB.crear_carpeta(data["titulo"],[],[],x.id)
        
        flash("Fondo creado correctamente","success")
        return redirect(url_for("contable.index_fondo"))
    else:
        # Obtener el primer campo con error
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]  # Primer error del campo
        # Mostrar el error
        flash(f"El campo {getattr(form, first_error_field).label.text} {first_error_message}", 'error')
        return render_template("contable/crear_fondo.html", form=form)


@bp.get("/fondos/<string:fondo_id>")
@role_required('Administrador', 'Colaborador')
def mostrar_fondo(fondo_id):
    form = FormularioNuevoIngreso()
    fond = fondo.conseguir_fondo_de_id(fondo_id)
    if not fond:
        return redirect(url_for('contable.index'))
    ingresos = ingresoDB.get_ingresos_del_fondo(fondo_id)
    return render_template("contable/detalle_fondo.html", fondo=fond,ingresos=ingresos,form=form)


@bp.post("/fondos/eliminar")
@role_required('Administrador', 'Colaborador')
def delete_fondo():
    fondo_id = request.form.get("fondo_id")
    fond = fondo.conseguir_fondo_de_id(fondo_id)
    if not fond:
        return redirect(url_for('contable.index'))
    
    # Check if there are any associated ingresos
    ingresos = ingresoDB.get_ingresos_del_fondo(fondo_id)
    if ingresos:
        flash("No se puede eliminar el fondo porque tiene ingresos asociados", "error")
        return redirect(url_for('contable.mostrar_fondo', fondo_id=fondo_id))
    
    # Delete the folder associated with the fondo
    if fond.carpeta:
        archivos_adminDB.eliminar_carpeta(fond.carpeta.id)
    
    fondo.delete_fondo(fondo_id)
    flash("Fondo eliminado correctamente", "success")
    return redirect(url_for('contable.index_fondo'))


@bp.post("/ingreso/<string:fondo_id>")
@role_required('Administrador', 'Colaborador')
def crear_ingreso(fondo_id):
    fond = fondo.conseguir_fondo_de_id(fondo_id)
    if not fond:
        return redirect(url_for('contable.index'))

    if True:
        data = request.form.to_dict()
        if data["monto"] == "0":
            flash("El monto no puede ser 0", "error")
            return redirect(url_for("contable.mostrar_fondo",fondo_id=fondo_id))
        if not data["monto"]:
            flash("El monto no puede estar vacio", "error")
            return redirect(url_for("contable.mostrar_fondo",fondo_id=fondo_id))
        data["receptor_id"] = fondo_id
        csrf_token = data.pop("csrf_token", None)
        file = data.pop("file", None)
        #subir archivo
        if 'file' in request.files and request.files['file'].filename != '':
            archivo = request.files['file']
            id_carpeta = archivos_adminDB.get_carpeta_by_nombre(fond.titulo).id
            data['archivo_id'] = archivos_adminDB.guardar_archivo_en_carpeta(id_carpeta, archivo).id
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


@bp.post("/ingreso/delete")
@role_required('Administrador', 'Colaborador')
def delete_ingreso():
    id = request.form.get("ingreso_id")
    ingreso = ingresoDB.conseguir_ingreso_de_id(id)
    if not ingreso:
        return redirect(url_for("contable.index"))
    
    fondo_id = ingreso.receptor_id
    fond = fondo.conseguir_fondo_de_id(fondo_id)
    if not fond:
        return redirect(url_for('contable.index'))
    
    # Restar el monto del ingreso del saldo del fondo
    fond.saldo -= Decimal(ingreso.monto)
    fondo.modificar_fondo(fondo_id, saldo=fond.saldo)
    
    # Eliminar archivo asociado si existe
    archivo_id = None
    if ingreso.archivo_id:
        archivo_id = ingreso.archivo_id
    ingresoDB.delete_ingreso(id)
    if archivo_id:
        archivos_adminDB.eliminar_archivo(archivo_id)
    flash("Ingreso eliminado correctamente", "success")
    return redirect(url_for("contable.mostrar_fondo", fondo_id=fondo_id))
@bp.get("/ingreso/descargar/<int:id>")
@role_required('Administrador', 'Colaborador')
def descargar_ingreso(id):
    ingreso = ingresoDB.conseguir_ingreso_de_id(id)
    if not ingreso:
        return redirect(url_for("contable.index"))
    archivo = ingreso.archivo_id
    if not archivo:
        return redirect(url_for("contable.index"))
    id_carpeta = archivos_adminDB.get_carpeta_by_nombre(ingreso.receptor.titulo).id

    directorio = archivos_adminDB.conseguir_directorio(id_carpeta)
    archivo = archivos_adminDB.conseguir_archivo_de_id(ingreso.archivo_id)
    
    filepath = os.path.join(directorio, archivo.nombre)
    if not os.path.exists(filepath):
        flash("Archivo no encontrado", "error")
        return redirect(url_for('contable.mostrar_fondo',fondo_id=ingreso.receptor_id))

    return send_from_directory(directorio, archivo.nombre, as_attachment=False)


@bp.get("/legajos")
@role_required('Administrador', 'Colaborador', 'Personal')
def get_legajos():
    params = request.args.to_dict()
    page = request.args.get("page", 1, type=int)
    per_page = 10
    if current_user.rol == "Personal":
        legajos = Legajo.query.filter(Legajo.area_id == current_user.empleado.area_id).paginate(page=page,per_page=per_page,error_out=True)
    else:
        legajos = legajoDB.list_legajos(page, per_page,None,None,None,None,None,True)
    #legajos = [legajo for legajo in legajos if legajo.necesita_facturacion]

    forms = {}
    for legajo in legajos:
        forms[legajo.id] = UploadDocumentoForm(legajo_id=legajo.id)
    
    resultado = []

    for legajo in legajos:
        documentos = {doc.tipo_documento.nombre: doc for doc in legajo.documento}
        distribuciones = distribucionDB.list_distribuciones_by_legajo(legajo.id)
        if((params.get('filtro') and params['filtro'] =="SinDistribucion" and distribuciones == [] )or not params.get('filtro')):
            resultado.append({
                "id": legajo.id,
                "cliente": legajo.cliente,
                "documentos": documentos,
                "distribuciones" : distribuciones
            })
    form = DownloadForm()
    return render_template("contable/legajos.html",legajos = resultado, forms=forms,formDescarga = form,paginacion = legajos)


@bp.get("/distribuciones/crear/<int:id>")
@role_required('Administrador', 'Colaborador')
def get_crear_distribucion(id):
    form = FormularioNuevaDistribucion()
    empleados = empleadoDB.list_empleados()
    
    # Relación empleados-areas (simulada aquí, pero ajusta según tu base de datos)
    empleados_por_area = {}
    for empleado in empleados:
        empleados_por_area.setdefault(empleado.area_id, []).append(empleado.id)
    distribucion_max_id = distribucionDB.get_max_id()
    return render_template("contable/crear_distribucion.html", form = form,empleados_por_area=empleados_por_area, id_legajo = id, distribucion_max_id = distribucion_max_id)


@bp.post("/distribuciones/crear/<int:id>")
@role_required('Administrador', 'Colaborador')
def crear_distribucion(id):
    form = FormularioNuevaDistribucion(request.form)
    if form.validate_on_submit():
        data = request.form.to_dict()
        empleados_ids = form.empleados_seleccionados.data
        porcentaje_empleados = round(float(data["porcentaje_empleados"]) * 0.01, 4)
        if porcentaje_empleados == 0 and len(empleados_ids) > 0:
            flash("El porcentaje de empleados no puede ser 0 si se seleccionaron empleados", "error")
            return redirect(url_for("contable.get_crear_distribucion",id=id))
        if porcentaje_empleados > 0 and len(empleados_ids) == 0:
            flash("Debe seleccionar empleados si el porcentaje de empleados es mayor a 0", "error")
            return redirect(url_for("contable.get_crear_distribucion",id=id))

        #Validaciones
        csrf_token = data.pop("csrf_token", None)
        data["legajo_id"] = id
        emp = data.pop("empleados_seleccionados", None)
        #Crea la distribucion
        nueva_distribucion = distribucionDB.create_distribucion(**data)
        #Sumo lo indicado al saldo de las areas
        area_ganancias = int(data["ganancias_de_id"])
        area_costos = int(data["costos_de_id"])
        porcentaje_area = round(float(data["porcentaje_area"]) * 0.01, 4)
        porcentaje_comisiones = round(float(data["porcentaje_comisiones"]) * 0.01, 4)
        monto_a_distribuir = round(float(data["monto_a_distribuir"]), 4)
        costos = round(float(data["costos"]), 2)
        areaDB.sumar_saldo_area(area_costos, costos)
        monto_modificado = round((monto_a_distribuir * (1 - porcentaje_comisiones)) - costos, 4)
        areaDB.sumar_saldo_area(area_ganancias, round((monto_modificado * porcentaje_area) * (1 - porcentaje_empleados), 2))
        areaCidepint = areaDB.get_area_by_name("CIDEPINT")
        areaDB.sumar_saldo_area(areaCidepint.id, round((monto_modificado * (1 - porcentaje_area)) * 0.95, 2))
        
        # Obtener todos los colaboradores y admin
        empleados = empleadoDB.list_empleados()
        colaboradores = [empleado for empleado in empleados if empleado.user.rol == "Colaborador" or empleado.user.rol == "Administrador"]
        for colaborador in colaboradores:
            colaborador.saldo += Decimal(round((((monto_modificado * (1 - porcentaje_area)) * 0.05) / len(colaboradores)), 2))
        
        # Relación con los empleados
        if empleados_ids:
            monto_empleado = round(((monto_modificado * porcentaje_area) * (porcentaje_empleados)) / len(empleados_ids), 2)
            for empleado_id in empleados_ids:
                empleado = db.session.query(Empleado).get(empleado_id)
                if empleado:
                    empleado.saldo += Decimal(monto_empleado)
                    empleado_distribucion = Empleado_Distribucion(
                        empleado_id=empleado.id,
                        distribucion_id=nueva_distribucion.id
                    )
                    db.session.add(empleado_distribucion) 
        db.session.commit()
        #Redirige a la lista de distribuciones
        flash("Distribución creada correctamente","success")
        return redirect(url_for("contable.get_legajos"))
    else:
        # Obtener el primer campo con error
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]
        flash(f"Error en el campo {first_error_field}: {first_error_message}", 'error')
        return redirect(url_for("contable.get_crear_distribucion",id=id,form=form))


@bp.get("/distribuciones/<int:id>")
@role_required('Administrador', 'Colaborador')
def get_distribuciones(id):
    data = distribucionDB.list_distribuciones_by_legajo(id)
    legajo = legajoDB.find_legajo_by_id(id)
    return render_template("contable/listar_distribuciones.html",distribuciones = data, legajo = legajo)


@bp.post("/distribuciones/delete")
def delete_distribucion():
    id = request.form.get("distribucion_id")
    distribucion = distribucionDB.get_distribucion(id)
    if not distribucion:
        return redirect(url_for("contable.get_legajos"))
    legajo_id = distribucion.legajo_id
    #Restar lo que se sumo
    area_ganancias = distribucion.ganancias_de_id
    area_costos = distribucion.costos_de_id
    porcentaje_area = Decimal(distribucion.porcentaje_area * 0.01)
    porcentaje_empleados = Decimal(distribucion.porcentaje_empleados * 0.01)
    porcentaje_comisiones = Decimal(distribucion.porcentaje_comisiones * 0.01)
    monto_a_distribuir = distribucion.monto_a_distribuir
    costos = distribucion.costos
    areaDB.sumar_saldo_area(area_costos, round(-costos, 2))
    monto_modificado = round((monto_a_distribuir * (1 - porcentaje_comisiones)) - costos, 2)
    areaDB.sumar_saldo_area(area_ganancias, round(-(monto_modificado * porcentaje_area) * (1 - porcentaje_empleados), 2))
    areaCidepint = areaDB.get_area_by_name("CIDEPINT")
    areaDB.sumar_saldo_area(areaCidepint.id, round(-(monto_modificado * Decimal(1 - porcentaje_area)) * Decimal(0.95), 2))
    empleados = empleadoDB.list_empleados()
    colaboradores = [empleado for empleado in empleados if empleado.user.rol == "Colaborador" or empleado.user.rol == "Administrador"]
    for colaborador in colaboradores:
        colaborador.saldo -= Decimal((((monto_modificado * Decimal(1 - porcentaje_area)) * Decimal(0.05)) / len(colaboradores)))

    empleados_ids = [ed.empleado_id for ed in distribucion.empleados_asociados]
    if empleados_ids:
        monto_empleado = ((monto_modificado * porcentaje_area) * (porcentaje_empleados)) / len(empleados_ids)
        for empleado_id in empleados_ids:
            empleado = db.session.query(Empleado).get(empleado_id)
            if empleado:
                empleado.saldo -= monto_empleado
                empleado_distribucion = db.session.query(Empleado_Distribucion).filter_by(
                empleado_id=empleado.id, distribucion_id=distribucion.id).first()
                if empleado_distribucion:
                    db.session.delete(empleado_distribucion)

    db.session.commit()
    distribucionDB.delete_distribucion(id)
    flash("Distribución eliminada correctamente","success")
    return redirect(url_for("contable.get_distribuciones",id=legajo_id))


@bp.get("/legajos/<int:id>/documentos")
@role_required('Administrador', 'Colaborador')
def get_documentosAdd(id):
    form = UploadDocumentoForm(legajo_id=id)
    form.tipo.data = "adicional"
    legajo = legajoDB.find_legajo_by_id(id)
    documentos = [doc for doc in legajo.documento if doc.tipo_documento.nombre == "Adicional"]
    delete_form = DeleteForm()
    return render_template("contable/legajo_adicionales.html",form = form,legajo = legajo,documentos = documentos, delete_form=delete_form)


@bp.post('/upload')
@role_required('Administrador', 'Colaborador')
def upload():
    file = request.files['file']
    tipo = request.form['tipo']
    legajo_id = request.form['legajo_id']
    if file.filename == '':# or not file.filename.endswith('.pdf'):
        flash("El archivo tiene que terner nombre o/y una extensión valida", "error")
        return redirect(url_for("contable.get_legajos"))
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
        old_file = None
        if tipo != 'adicional':
            old_file = find_documento(data)
        if old_file:
            old_documento_path = documentos_path / old_file.nombre_documento
            if old_documento_path.exists():
                old_documento_path.unlink()
                file.save(str(file_path))
                old_file.nombre_documento = file.filename
                db.session.commit()
                flash("Documento subido correctamente","success")
                return redirect(url_for("contable.get_legajos"))
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
            flash("Documento subido correctamente","success")
            if tipo == 'adicional':
                return redirect(url_for("contable.get_documentosAdd",id=legajo_id))
            return redirect(url_for("contable.get_legajos"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.post('/delete_document')
@role_required('Administrador', 'Colaborador')
def delete_document():
    documento_id = request.form.get("documento_id")
    documento = get_documento(documento_id)
    if documento is None:
        return jsonify({"error": "No se encontro el archivo"}), 404
    tipo = documento.tipo_documento.nombre
    filename = documento.nombre_documento

    # Ruta base de los documentos
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[4]
    documentos_path = project_root / "documentos" / tipo

    # Ruta completa del archivo
    file_path = documentos_path / filename

    # Verificar que el archivo exista
    if not file_path.exists():
        return jsonify({"error": "El archivo no existe"}), 404

    # Eliminar el archivo
    file_path.unlink()
    db.session.delete(documento)
    db.session.commit()
    if tipo == 'adicional':
        return redirect(url_for("contable.get_documentosAdd",id=documento.legajo_id))
    else:
        return redirect(url_for("contable.get_legajos"))


@bp.get('/download/<int:documento_id>')
@role_required('Administrador', 'Colaborador')
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
        as_attachment=False,
        download_name=filename  # Nombre que se verá al descargar
    )