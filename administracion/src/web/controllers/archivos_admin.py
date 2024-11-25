from datetime import datetime
import os
from administracion.src.core.servicios import archivos_admin as servicio_archivos
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from administracion.src.web.forms.carpeta_nueva import FormularioNuevaCarpeta

bp = Blueprint("archivos",__name__,url_prefix="/archivos")

@bp.get("/")
def index():
    anio_actual = datetime.now().year
    anio = request.args.get("anio", anio_actual)
    carpetas = servicio_archivos.listar_carpetas(anio)

    anios = list(range(2024,  anio_actual + 1))
    anios.reverse()
    return render_template("archivos_admin/lista_carpetas.html",carpetas=carpetas,anios=anios)


@bp.get("/carpeta/<int:id_carpeta>")
def ver_carpeta(id_carpeta):
    archivos = servicio_archivos.listar_archivos_de_carpeta(id_carpeta)
    carpeta = servicio_archivos.conseguir_carpeta_de_id(id_carpeta)
    anio = carpeta.fecha_ingreso.year

    if not carpeta:
        flash("Carpeta no encontrada", 'error')
        return redirect(url_for('archivos.index'))
    
    return render_template("archivos_admin/lista_archivos.html",archivos=archivos, carpeta=carpeta, anio=anio)


@bp.get("/carpeta/agregar")
def nueva_carpeta():
    form = FormularioNuevaCarpeta()

    return render_template("archivos_admin/nueva_carpeta.html",form=form)


@bp.post("/carpeta/agregar")
def agregar_carpeta():
    form = FormularioNuevaCarpeta(request.form)
    if form.validate_on_submit():
        data = request.form

        if servicio_archivos.chequear_nombre_carpeta_existente(data.get('nombre')):
            flash('Ya existe una carpeta con ese nombre', 'error')
            return render_template("archivos_admin/nueva_carpeta.html", form=form)
        carpeta = servicio_archivos.crear_carpeta(
                nombre=data.get('nombre'),
                usuarios_lee=data.get('usuarios_lee'),
                usuarios_edita=data.get('usuarios_edita'),
            )
        flash('Carpeta agregada correctamente', 'success')
        return redirect (url_for("archivos.ver_carpeta", id_carpeta=carpeta.id))
    else:
        # Obtener el primer campo con error
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]  # Primer error del campo
        # Mostrar el error
        flash(f"El campo {getattr(form, first_error_field).label.text} {first_error_message}", 'error')
        return render_template("archivos_admin/nueva_carpeta.html", form=form)


@bp.post("/carpeta/subir/<int:id_carpeta>")
def subir_archivo(id_carpeta: int):
    
    if 'archivo' in request.files and request.files['archivo'].filename != '':
        archivo = request.files['archivo']

        servicio_archivos.guardar_archivo_en_carpeta(id_carpeta, archivo)
        
        flash("Archivo subido correctamente", "success")
    else:
        flash(
            "Error en la subida del archivo, por favor intenta de nuevo",
            "error",
        )
    return redirect(url_for('archivos.ver_carpeta',id_carpeta=id_carpeta))

@bp.get("/descargar/<int:id_carpeta>/<int:id_archivo>")
def descargar_archivo(id_carpeta, id_archivo):
    directorio = servicio_archivos.conseguir_directorio(id_carpeta)
    archivo = servicio_archivos.conseguir_archivo_de_id(id_archivo)
    
    filepath = os.path.join(directorio, archivo.nombre)
    if not os.path.exists(filepath):
        flash("Archivo no encontrado", "error")
        return redirect(url_for('archivos.ver_carpeta',id_carpeta=id_carpeta))

    return send_from_directory(directorio, archivo.nombre)


@bp.post("/eliminar_archivo/<int:id_carpeta>")
def eliminar_archivo(id_carpeta):
    data = request.form
    print(f'Id del archivo: {data.get('id_archivo')}')
    if servicio_archivos.eliminar_archivo(id_archivo=data.get('id_archivo')):
        flash('Archivo eliminado correctamente', 'success')
    else:
        flash('Error al eliminar el archivo', 'error')
    return redirect(url_for('archivos.ver_carpeta',id_carpeta=id_carpeta))


@bp.post("/eliminar_carpeta")
def eliminar_carpeta():
    data = request.form
    print(f'Id de la carpeta: {data.get('id_carpeta')}')
    if servicio_archivos.eliminar_carpeta(id_carpeta=data.get('id_carpeta')):
        flash('Carpeta eliminada correctamente', 'success')
    else:
        flash('Error al eliminar la carpeta', 'error')
    return redirect(url_for('archivos.index'))