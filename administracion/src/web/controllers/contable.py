from administracion.src.core.fondos import fondo
from flask import Blueprint, render_template, request, redirect, url_for, flash
from administracion.src.web.forms.fondo_nuevo import FormularioNuevoFondo

bp = Blueprint("contable",__name__,url_prefix="/contable")

@bp.get("/")
def index():
    return render_template("contable/contable.html")

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

