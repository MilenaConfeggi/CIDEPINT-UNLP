from administracion.src.core.fondos import fondo
from flask import Blueprint, render_template, request, redirect, url_for, flash


bp = Blueprint("contable",__name__,url_prefix="/contable")

@bp.get("/")
def index():
    return render_template("contable/contable.html")