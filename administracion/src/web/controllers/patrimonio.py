import os
from administracion.src.core.servicios import patrimonio as servicio_patrimonio
from administracion.src.core.servicios import archivos_admin as servicio_archivos
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from administracion.src.web.forms.bien_nuevo import FormularioNuevoBien
from administracion.src.web.forms.bien_baja import FormularioBajaBien

bp = Blueprint("patrimonio",__name__,url_prefix="/patrimonio")

@bp.get("/")
def index():
    titulo = request.args.get("titulo")
    numero_inventario = request.args.get("numero_inventario")
    area = request.args.get("area")
    baja = request.args.get("baja", "Activos")
    page = request.args.get("page", 1, type=int)
    per_page = 10

    bienes = servicio_patrimonio.filtrar_bienes(
        titulo, numero_inventario, area, baja, page, per_page
    )

    form = FormularioBajaBien()

    return render_template("patrimonio/lista.html",bienes=bienes, form=form)


@bp.get("/<int:id_bien>")
def mostrar_bien(id_bien):
    bien = servicio_patrimonio.conseguir_bien_de_id(id_bien)
    if not bien:
        return redirect(url_for('patrimonio.index'))

    archivos = None

    return render_template("patrimonio/ver_bien.html", bien=bien,archivos=archivos)


@bp.get("/nuevo")
def nuevo_bien():
    form = FormularioNuevoBien()

    return render_template("patrimonio/formulario_nuevo.html", form=form)

@bp.post("/nuevo")
def crear_bien():
    form = FormularioNuevoBien()
    if form.validate_on_submit():
        data = request.form
        
        bien = servicio_patrimonio.crear_bien(
                titulo=data.get('titulo'),
                numero_inventario=data.get('numero_inventario'),
                anio=data.get('anio'),
                institucion=data.get('institucion'),
                descripcion=data.get('descripcion'),
            )

        if form.archivos_adjuntos.data:
            servicio_patrimonio.guardar_archivos_de_bien(bien.id, form.archivos_adjuntos.data)

        flash('Bien registrado correctamente', 'success')
        return redirect (url_for("patrimonio.index"))
    else:
        # Obtener el primer campo con error
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]  # Primer error del campo
        # Mostrar el error
        flash(f"El campo {getattr(form, first_error_field).label.text} {first_error_message}", 'error')
        return render_template("patrimonio/formulario_nuevo.html", form=form)


@bp.post("/dar_de_baja")
def dar_de_baja_bien():
    form = FormularioBajaBien(request.form)
    if form.validate_on_submit():
        data = request.form
        servicio_patrimonio.dar_de_baja_bien(
                id_bien=data.get('id_bien'),
                motivo_baja=data.get('motivo_baja'),
            )
        flash('Bien dado de baja correctamente', 'success')
        return redirect (url_for("patrimonio.index"))
    else:
        # Obtener el primer campo con error
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]  # Primer error del campo
        # Mostrar el error
        flash(f"El campo {getattr(form, first_error_field).label.text} {first_error_message}", 'error')
        return render_template("patrimonio/formulario_nuevo.html", form=form)


@bp.post("/restaurar")
def restaurar_bien():
    servicio_patrimonio.restaurar_bien(id_bien=request.form.get('id_bien'))
    flash('Bien restaurado correctamente', 'success')
    return redirect (url_for("patrimonio.index"))

@bp.get("/descargar/<int:id_bien>/<int:id_archivo>")
def descargar_archivo(id_bien, id_archivo):
    directorio = servicio_patrimonio.conseguir_directorio(id_bien)
    archivo = servicio_archivos.conseguir_archivo_de_id(id_archivo)
    
    filepath = os.path.join(directorio, archivo.nombre)
    if not os.path.exists(filepath):
        flash("Archivo no encontrado", "error")
        return redirect(url_for('patrimonio.mostrar_bien',id_bien=id_bien))

    return send_from_directory(directorio, archivo.nombre, as_attachment=True)


@bp.post("/carpeta/subir/<int:id_bien>")
def subir_archivo(id_bien: int):
    
    if 'archivo' in request.files and request.files['archivo'].filename != '':
        archivo = [request.files['archivo']]

        servicio_patrimonio.guardar_archivos_de_bien(id_bien, archivo)
        
        flash("Archivo subido correctamente", "success")
    else:
        flash(
            "Error en la subida del archivo, por favor intenta de nuevo",
            "error",
        )
    return redirect(url_for('patrimonio.mostrar_bien',id_bien=id_bien))


@bp.post("/eliminar_archivo/<int:id_bien>")
def eliminar_archivo(id_bien):
    data = request.form
    print(f'Id del archivo: {data.get('id_archivo')}')
    if servicio_archivos.eliminar_archivo(id_archivo=data.get('id_archivo')):
        flash('Archivo eliminado correctamente', 'success')
    else:
        flash('Error al eliminar el archivo', 'error')
    return redirect(url_for('patrimonio.mostrar_bien',id_bien=id_bien))


@bp.get("/editar/<int:id_bien>")
def editar_bien(id_bien):
    bien = servicio_patrimonio.conseguir_bien_de_id(id_bien)

    if not bien:
        flash("Bien no encontrado", 'error')
        return redirect(url_for('patrimonio.index'))
    
    form = FormularioNuevoBien(obj=bien)

    return render_template("patrimonio/formulario_editar.html", form=form, id_bien=id_bien)


@bp.post("/editar/<int:id_bien>")
def actualizar_bien(id_bien):
    form = FormularioNuevoBien()
    if form.validate_on_submit():
        data = request.form
        bien = servicio_patrimonio.conseguir_bien_de_id(id_bien)

        if not bien:
            flash("Bien no encontrado", 'error')
            return redirect(url_for('patrimonio.index'))
        
        bien = servicio_patrimonio.editar_bien(
                id_bien=id_bien,
                titulo=data.get('titulo'),
                numero_inventario=data.get('numero_inventario'),
                anio=data.get('anio'),
                institucion=data.get('institucion'),
                descripcion=data.get('descripcion'),
            )

        flash('Bien actualizado correctamente', 'success')
        return redirect (url_for("patrimonio.mostrar_bien",id_bien=bien.id))
    else:
        # Obtener el primer campo con error
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]  # Primer error del campo
        # Mostrar el error
        flash(f"El campo {getattr(form, first_error_field).label.text} {first_error_message}", 'error')
        return render_template("patrimonio/formulario_editar.html", form=form, id_bien=id_bien)