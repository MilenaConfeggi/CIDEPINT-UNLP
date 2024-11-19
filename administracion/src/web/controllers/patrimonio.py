from administracion.src.core.servicios import patrimonio
from flask import Blueprint, render_template, request, redirect, url_for, flash


bp = Blueprint("patrimonio",__name__,url_prefix="/patrimonio")

@bp.get("/")
def index():
    bienes = patrimonio.listar_bienes()
    return render_template("landing_page.html",bienes=bienes)

'''
@bp.get("/")
def index():
    name = request.args.get("name")
    surname = request.args.get("surname")
    dni = request.args.get("dni")
    professionals = request.args.get("professionals")
    page = request.args.get("page", 1, type=int)
    order_by = request.args.get("order_by")
    order = request.args.get("order")
    per_page = 5

    # Execute the query with filters and pagination
    bienes = service.filtrar_bienes(
        name, surname, dni, professionals, page, per_page, order_by, order
    )

    return render_template("bienes/index.html",bienes=bienes)
'''