from administracion.src.core.servicios import patrimonio as servicio_patrimonio
from flask import Blueprint, render_template, request, redirect, url_for, flash


bp = Blueprint("patrimonio",__name__,url_prefix="/patrimonio")

@bp.get("/")
def index():
    titulo = request.args.get("titulo")
    numero_inventario = request.args.get("numero_inventario")
    area = request.args.get("area")
    page = request.args.get("page", 1, type=int)
    per_page = 10

    bienes = servicio_patrimonio.filtrar_bienes(
        titulo, numero_inventario, area, page, per_page
    )

    return render_template("patrimonio/lista.html",bienes=bienes)


@bp.get("/<int:bien_id>")
def mostrar_bien(bien_id):
    bien = servicio_patrimonio.conseguir_bien_de_id(bien_id)
    if not bien:
        return redirect(url_for('patrimonio.index'))

    archivos = None

    return render_template("patrimonio/ver_bien.html", bien=bien,archivos=archivos)