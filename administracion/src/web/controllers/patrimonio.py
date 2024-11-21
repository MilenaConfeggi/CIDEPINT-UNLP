from administracion.src.core.servicios import patrimonio as servicio_patrimonio
from flask import Blueprint, render_template, request, redirect, url_for, flash
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


@bp.get("/<int:bien_id>")
def mostrar_bien(bien_id):
    bien = servicio_patrimonio.conseguir_bien_de_id(bien_id)
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
    form = FormularioNuevoBien(request.form)
    if form.validate_on_submit():
        data = request.form
        
        servicio_patrimonio.crear_bien(
                titulo=data.get('titulo'),
                numero_inventario=data.get('numero_inventario'),
                anio=data.get('anio'),
                institucion=data.get('institucion'),
                descripcion=data.get('descripcion'),
            )
        flash('Bien registrado correctamente', 'success')
        return redirect (url_for("patrimonio.index"))
    else:
        # Obtener el primer campo con error
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]  # Primer error del campo
        # Mostrar el error
        flash(f"El campo {getattr(form, first_error_field).label.text} {first_error_message}", 'danger')
        return render_template("patrimonio/formulario_nuevo.html", form=form)


@bp.post("/dar_de_baja")
def dar_de_baja_bien():
    form = FormularioBajaBien(request.form)
    if form.validate_on_submit():
        data = request.form
        print(f'Id del bien: {data.get('bien_id')}')
        servicio_patrimonio.dar_de_baja_bien(
                bien_id=data.get('bien_id'),
                motivo_baja=data.get('motivo_baja'),
            )
        flash('Bien dado de baja correctamente', 'success')
        return redirect (url_for("patrimonio.index"))
    else:
        # Obtener el primer campo con error
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]  # Primer error del campo
        # Mostrar el error
        flash(f"El campo {getattr(form, first_error_field).label.text} {first_error_message}", 'danger')
        return render_template("patrimonio/formulario_nuevo.html", form=form)