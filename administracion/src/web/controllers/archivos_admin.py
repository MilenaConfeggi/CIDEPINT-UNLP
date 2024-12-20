from datetime import datetime
import os
from administracion.src.core.servicios import archivos_admin as servicio_archivos
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import current_user
from administracion.src.web.forms.carpeta_nueva import FormularioNuevaCarpeta
from administracion.src.web.controllers.roles import role_required
from administracion.src.core.servicios import personal as servicio_personal

bp = Blueprint("archivos",__name__,url_prefix="/archivos")

@bp.get("/")
@role_required('Administrador', 'Colaborador', 'Personal') 
def index():
    anio_actual = datetime.now().year
    anio = request.args.get("anio", anio_actual)
    carpetas = servicio_archivos.listar_carpetas(anio)

    anios = list(range(2024,  anio_actual + 1))
    anios.reverse()
    return render_template("archivos_admin/lista_carpetas.html",carpetas=carpetas,anios=anios)


@bp.get("/carpeta/<int:id_carpeta>")
@role_required('Administrador', 'Colaborador', 'Personal') 
def ver_carpeta(id_carpeta):
    archivos = servicio_archivos.listar_archivos_de_carpeta(id_carpeta)
    carpeta = servicio_archivos.conseguir_carpeta_de_id(id_carpeta)
    anio = carpeta.fecha_ingreso.year

    if not carpeta:
        flash("Carpeta no encontrada", 'error')
        return redirect(url_for('archivos.index'))
    
    if current_user.rol == 'Personal' and current_user not in carpeta.usuarios_leen:
        flash("No tienes permisos para ver esta carpeta", 'error')
        return redirect(url_for('archivos.index'))
    
    if current_user.rol == 'Personal':
        puede_editar = current_user in carpeta.usuarios_editan
    else:
        puede_editar = True

    return render_template("archivos_admin/lista_archivos.html",archivos=archivos, carpeta=carpeta, anio=anio, puede_editar=puede_editar)


@bp.get("/carpeta/agregar")
@role_required('Administrador', 'Colaborador') 
def nueva_carpeta():
    form = FormularioNuevaCarpeta()
    usuarios = servicio_personal.listar_usuarios_personal()

    return render_template("archivos_admin/nueva_carpeta.html",form=form, users=usuarios)


@bp.post("/carpeta/agregar")
@role_required('Administrador', 'Colaborador')
def agregar_carpeta():
    form = FormularioNuevaCarpeta()

    if form.validate_on_submit():
        data = request.form

        if servicio_archivos.chequear_nombre_carpeta_existente(data.get('nombre')):
            flash('Ya existe una carpeta con ese nombre', 'error')
            return render_template("archivos_admin/nueva_carpeta.html", form=form)
        
        usuarios_leen = set()
        usuarios_editan = set()
        for permiso in form.permisos.data:
            usuarios_leen.add(servicio_personal.conseguir_usuario_de_id(permiso["user_id"]))
            if permiso["permiso"] == 'editar':
                usuarios_editan.add(servicio_personal.conseguir_usuario_de_id(permiso["user_id"]))
    
        carpeta = servicio_archivos.crear_carpeta(
                nombre=data.get('nombre'),
                usuarios_leen=list(usuarios_leen),
                usuarios_editan=list(usuarios_editan),
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
@role_required('Administrador', 'Colaborador', 'Personal')
def subir_archivo(id_carpeta: int):
    if current_user.rol == 'Personal' and current_user not in servicio_archivos.conseguir_carpeta_de_id(id_carpeta).usuarios_editan:
        flash("No tienes permisos para editar esta carpeta", 'error')
        return redirect(url_for('archivos.ver_carpeta',id_carpeta=id_carpeta))

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
@role_required('Administrador', 'Colaborador', 'Personal')
def descargar_archivo(id_carpeta, id_archivo):
    if current_user.rol == 'Personal' and current_user not in servicio_archivos.conseguir_carpeta_de_id(id_carpeta).usuarios_leen:
        flash("No tienes permisos para descargar archivos de esta carpeta", 'error')
        return redirect(url_for('archivos.ver_carpeta',id_carpeta=id_carpeta))
    
    directorio = servicio_archivos.conseguir_directorio(id_carpeta)
    archivo = servicio_archivos.conseguir_archivo_de_id(id_archivo)
    
    filepath = os.path.join(directorio, archivo.nombre)
    if not os.path.exists(filepath):
        flash("Archivo no encontrado", "error")
        return redirect(url_for('archivos.ver_carpeta',id_carpeta=id_carpeta))

    return send_from_directory(directorio, archivo.nombre, as_attachment=True)


@bp.post("/eliminar_archivo/<int:id_carpeta>")
@role_required('Administrador', 'Colaborador', 'Personal')
def eliminar_archivo(id_carpeta):
    if current_user.rol == 'Personal' and current_user not in servicio_archivos.conseguir_carpeta_de_id(id_carpeta).usuarios_editan:
        flash("No tienes permisos para editar esta carpeta", 'error')
        return redirect(url_for('archivos.ver_carpeta',id_carpeta=id_carpeta))
    
    data = request.form
    if servicio_archivos.eliminar_archivo(id_archivo=data.get('id_archivo')):
        flash('Archivo eliminado correctamente', 'success')
    else:
        flash('Error al eliminar el archivo', 'error')
    return redirect(url_for('archivos.ver_carpeta',id_carpeta=id_carpeta))


@bp.post("/eliminar_carpeta")
@role_required('Administrador', 'Colaborador') 
def eliminar_carpeta():
    data = request.form
    if servicio_archivos.eliminar_carpeta(id_carpeta=data.get('id_carpeta')):
        flash('Carpeta eliminada correctamente', 'success')
    else:
        flash('Error al eliminar la carpeta', 'error')
    return redirect(url_for('archivos.index'))


@bp.get("/carpeta/editar/<int:id_carpeta>")
@role_required('Administrador', 'Colaborador') 
def editar_carpeta(id_carpeta):
    carpeta = servicio_archivos.conseguir_carpeta_de_id(id_carpeta)

    if not carpeta:
        flash("Carpeta no encontrada", 'error')
        return redirect(url_for('archivos.index'))
    
    form = FormularioNuevaCarpeta(obj=carpeta)

    for user in carpeta.usuarios_leen:
        if user not in carpeta.usuarios_editan:
            form.permisos.append_entry({'user_id': user.id, 'permiso': 'ver'})
    for user in carpeta.usuarios_editan:
        form.permisos.append_entry({'user_id': user.id, 'permiso': 'editar'})

    usuarios = servicio_personal.listar_usuarios_personal()

    return render_template("archivos_admin/editar_carpeta.html",form=form,id_carpeta=id_carpeta, users=usuarios)


@bp.post("/carpeta/editar/<int:id_carpeta>")
@role_required('Administrador', 'Colaborador') 
def actualizar_carpeta(id_carpeta):
    form = FormularioNuevaCarpeta(request.form)
    if form.validate_on_submit():
        data = request.form
        carpeta = servicio_archivos.conseguir_carpeta_de_id(id_carpeta)
        if not carpeta:
            flash("Carpeta no encontrada", 'error')
            return redirect(url_for('archivos.index'))
        if carpeta.nombre != data.get('nombre'):
            if servicio_archivos.chequear_nombre_carpeta_existente(data.get('nombre')):
                flash('Ya existe una carpeta con ese nombre', 'error')
                return render_template("archivos_admin/editar_carpeta.html", form=form,id_carpeta=id_carpeta)
        
        usuarios_leen = set()
        usuarios_editan = set()
        for permiso in form.permisos.data:
            usuarios_leen.add(servicio_personal.conseguir_usuario_de_id(permiso["user_id"]))
            if permiso["permiso"] == 'editar':
                usuarios_editan.add(servicio_personal.conseguir_usuario_de_id(permiso["user_id"]))
        
        carpeta = servicio_archivos.editar_carpeta(
                id_carpeta=id_carpeta,
                nombre=data.get('nombre'),
                usuarios_leen=list(usuarios_leen),
                usuarios_editan=list(usuarios_editan),
            )
        flash('Carpeta editada correctamente', 'success')
        return redirect (url_for("archivos.ver_carpeta", id_carpeta=carpeta.id))
    else:
        # Obtener el primer campo con error
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]  # Primer error del campo
        # Mostrar el error
        flash(f"El campo {getattr(form, first_error_field).label.text} {first_error_message}", 'error')
        return render_template("archivos_admin/editar_carpeta.html", form=form,id_carpeta=id_carpeta)