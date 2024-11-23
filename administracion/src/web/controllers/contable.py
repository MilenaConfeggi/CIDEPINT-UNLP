from administracion.src.core.fondos import fondo
from flask import Blueprint, render_template, request, redirect, url_for, flash


bp = Blueprint("contable",__name__,url_prefix="/contable")

@bp.get("/")
def index():
    return render_template("contable/contable.html")

@bp.get("/fondos")
def get_crear_fondo():
    return render_template("contable/crear_fondo.html")

@bp.post("/fondos")
def crear_fondo():
    data = request.form.to_dict()
    fondo.create_fondo(**data)
    flash("Fondo creado correctamente")
    return redirect(url_for("contable.index_contable"))

