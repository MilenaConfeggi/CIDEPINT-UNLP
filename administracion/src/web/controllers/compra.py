from flask import Blueprint, render_template
from administracion.src.core.compras.compra import listar_compras 

bp = Blueprint("compra",__name__,url_prefix="/compra")

@bp.get("/")
def index():
    compras = listar_compras()
    print(compras)
    return render_template("compras/lista.html", compras=compras)