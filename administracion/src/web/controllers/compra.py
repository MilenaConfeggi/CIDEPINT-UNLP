from flask import Blueprint, render_template, request, redirect, flash, url_for, Response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from flask_login import current_user
from administracion.src.core.compras.compra import filtrar_compras, buscar_compra, filtrar_compras_descargadas, crear_compra
from administracion.src.core.proveedores.proveedor import filtrar_proveedores, chequeo_razon_social_existente, crear_proveedor, borrar_proveedor, actualizar_proveedor, buscar_proveedor
from administracion.src.web.forms.form_agregar_proveedor import form_agregar_proveedor
from administracion.src.web.forms.form_editar_proveedor import form_editar_proveedor
from administracion.src.web.forms.form_agregar_compra import form_agregar_compra
from administracion.src.web.controllers.roles import role_required
from administracion.src.core.servicios.personal import listar_empleados, listar_areas, conseguir_area_de_id, conseguir_empleado_de_id
from administracion.src.core.fondos.fondo import listar_fondos, conseguir_fondo_de_id

bp = Blueprint("compra",__name__,url_prefix="/compra")

@bp.get("/")
@role_required('Administrador', 'Colaborador', 'Personal') 
def index():
    return render_template("compras/inicio.html", rol=current_user.empleado.rol)

@bp.get("/lista_proveedores")
@role_required('Administrador', 'Colaborador') 
def lista_proveedores():

    razon_social = request.args.get("razon_social")
    contacto = request.args.get("contacto")
    page = request.args.get("page", 1, type=int)
    per_page = 10

    proveedores = filtrar_proveedores(
        razon_social, contacto, page, per_page
    )

    return render_template("compras/listado_proveedores.html", proveedores=proveedores)

@bp.get("/agregar_proveedor")
@role_required('Administrador', 'Colaborador') 
def agregar_proveedor():
    form = form_agregar_proveedor()
    return render_template("compras/creacion_proveedor.html", form=form)

@bp.post("/agregando_proveedor")
@role_required('Administrador', 'Colaborador') 
def agregando_proveedor():
    form = form_agregar_proveedor(request.form)
    if form.validate_on_submit():

        if chequeo_razon_social_existente(form.razon_social.data):
            flash(
                "La razon social ingresada ya se encuentra registrada en el sistema", "danger"
            )
            return render_template("compras/creacion_proveedor.html", form=form)

        crear_proveedor(
            form.razon_social.data,
            form.contacto.data,
        )
        flash("Proveedor agregado correctamente", "success")
        return redirect(url_for("compra.lista_proveedores"))
    else:
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]
        flash(
            f"Error en el campo {getattr(form, first_error_field).label.text}: {
              first_error_message}",
            "danger",
        )
        return render_template("compras/creacion_proveedor.html", form=form)
    
@bp.get("/editar_proveedor/<int:id_proveedor>")
@role_required('Administrador', 'Colaborador') 
def editar_proveedor(id_proveedor):
    proveedor = buscar_proveedor(id_proveedor)
    if not proveedor:
        return redirect(url_for("compra.lista_proveedores"))
    form = form_editar_proveedor(obj=proveedor)
    return render_template("compras/edicion_proveedor.html", form=form, proveedor=proveedor)

@bp.post("/editando_proveedor/<int:id_proveedor>")
@role_required('Administrador', 'Colaborador') 
def editando_proveedor(id_proveedor):
    proveedor = buscar_proveedor(id_proveedor)
    if not proveedor:
        flash("Proveedor no encontrado", "danger")
        return redirect(url_for("compra.lista_proveedores"))

    form = form_editar_proveedor(request.form, obj=proveedor)

    if form.validate_on_submit():
        razon_social = form.razon_social.data
        contacto = form.contacto.data

        if razon_social != proveedor.razon_social and chequeo_razon_social_existente(form.razon_social.data):
            flash(
                "La razon social ingresada ya se encuentra registrada en el sistema", "danger"
            )
            return render_template("compras/edicion_proveedor.html", form=form, proveedor=proveedor)

        actualizar_proveedor(id_proveedor, razon_social, contacto)

        flash("Proveedor actualizado exitosamente", "success")
        return redirect(url_for("compra.lista_proveedores"))
    else:
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]
        flash(
            f"Error en el campo {getattr(form, first_error_field).label.text}: {
              first_error_message}",
            "danger",
        )
        return render_template("compras/edicion_proveedor.html", form=form, proveedor=proveedor)

@bp.post("/eliminar_proveedor/<int:id_proveedor>")
@role_required('Administrador', 'Colaborador') 
def eliminar_proveedor(id_proveedor):
    mensaje = ""
    estado = ""
    mensaje, estado = borrar_proveedor(id_proveedor, mensaje, estado)
    flash(mensaje, estado)
    return redirect(url_for("compra.lista_proveedores"))

@bp.get("/lista_compras")
@role_required('Administrador', 'Colaborador', 'Personal')
def lista_compras():

    fecha_menor = request.args.get("fecha_menor")
    fecha_mayor = request.args.get("fecha_mayor")
    estado = request.args.get("estado")
    page = request.args.get("page", 1, type=int)
    per_page = 10
    compras = filtrar_compras(
        fecha_menor, fecha_mayor, estado, current_user.empleado.rol, current_user.empleado.area_id, page, per_page
    )

    return render_template("compras/listado_compras.html", compras=compras, rol=current_user.empleado.rol) 

@bp.get("/ver_compra/<int:id_compra>")
@role_required('Administrador', 'Colaborador', 'Personal')
def ver_compra(id_compra):
    compra = buscar_compra(id_compra)
    if not compra:
        return redirect(url_for('compra.lista_compras'))
    return render_template("compras/ver_compra.html", compra=compra)

@bp.get("/descargar_compras_excel")
@role_required('Administrador', 'Colaborador')
def descargar_compras_excel():

    # Retrieve filters from the request
    fecha_menor = request.args.get("fecha_menor")
    fecha_mayor = request.args.get("fecha_mayor")
    estado = request.args.get("estado")
    
    # Fetch all items based on the filters (no pagination)
    compras = filtrar_compras_descargadas(
        fecha_menor, fecha_mayor, estado, current_user.empleado.rol, current_user.empleado.area_id
    )

    # Prepare CSV data
    def generate_csv():

        data = [
            ["Fecha", "Descripcion", "Estado", "Numero de Factura", "Fuentes de financiamiento"]
        ]
        for compra in compras:
            fondos = "; ".join(fondo.titulo for fondo in compra.fondos)
            empleados = "; ".join(f"{empleado.nombre} {empleado.apellido}" for empleado in compra.empleados)
            areas = "; ".join(area.nombre for area in compra.areas)
            fuentes = "; ".join([fondos, empleados, areas])
            data.append([compra.fecha, compra.descripcion, compra.estado.value, compra.numero_factura, fuentes])

        # Write CSV rows
        for row in data:
            yield ", ".join(map(str, row)) + "\n"

    # Return CSV response
    return Response(
        generate_csv(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=lista_compras.csv"},
    )

@bp.get("/descargar_compras_pdf")
@role_required('Administrador', 'Colaborador')
def descargar_compras_pdf():
    
    # Retrieve filters from the request
    fecha_menor = request.args.get("fecha_menor")
    fecha_mayor = request.args.get("fecha_mayor")
    estado = request.args.get("estado")
    
    # Fetch all items based on the filters (no pagination)
    compras = filtrar_compras_descargadas(
        fecha_menor, fecha_mayor, estado, current_user.empleado.rol, current_user.empleado.area_id
    )
    
    # Prepare PDF data
    def generate_pdf():
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Set up the PDF header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, height - 30, "Fecha")
        c.drawString(150, height - 30, "Descripcion")
        c.drawString(250, height - 30, "Estado")
        c.drawString(300, height - 30, "Numero de Factura")
        c.drawString(425, height - 30, "Fuentes de financiamiento")
        
        y_position = height - 50
        
        # Write the data to the PDF
        c.setFont("Helvetica", 10)
        for compra in compras:
            fondos = "; ".join(fondo.titulo for fondo in compra.fondos)
            empleados = "; ".join(f"{empleado.nombre} {empleado.apellido}" for empleado in compra.empleados)
            areas = "; ".join(area.nombre for area in compra.areas)
            fuentes = "; ".join([fondos, empleados, areas])
            c.drawString(30, y_position, str(compra.fecha))
            c.drawString(150, y_position, compra.descripcion)
            c.drawString(250, y_position, compra.estado.value)
            c.drawString(300, y_position, compra.numero_factura)
            c.drawString(425, y_position, fuentes)
            y_position -= 15
            
            # Check if the page is full
            if y_position < 40:
                c.showPage()  # Create a new page
                y_position = height - 30
                # Recreate header on new page
                c.setFont("Helvetica-Bold", 12)
                c.drawString(30, y_position, "Fecha")
                c.drawString(150, y_position, "Descripcion")
                c.drawString(250, y_position, "Estado")
                c.drawString(300, y_position, "Numero de Factura")
                c.drawString(425, y_position, "Fuentes de financiamiento")
                y_position -= 20
        
        # Finalize the PDF
        c.save()
        buffer.seek(0)
        return buffer
    
    # Return PDF response
    pdf_buffer = generate_pdf()
    return Response(
        pdf_buffer,
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment;filename=lista_compras.pdf"},
    )

@bp.get("/agregar_compra")
@role_required('Administrador', 'Colaborador')
def agregar_compra():
    form = form_agregar_compra()
    areas = listar_areas()
    empleados = listar_empleados()
    fondos = listar_fondos()
    return render_template("compras/creacion_compra.html", form=form, areas=areas, empleados=empleados, fondos=fondos)

@bp.post("/agregando_compra")
@role_required('Administrador', 'Colaborador')
def agregando_compra():
    form = form_agregar_compra(request.form)
    if form.validate_on_submit():
        monto = 0
        fondos, empleados, areas = [], [], []
        for area in form.areas.data:
            area_obj = conseguir_area_de_id(area["id_area"])
            if area["monto"] > area_obj.saldo:
                flash("El monto de un área no puede ser superior a su saldo", "danger")
                return render_template("compras/creacion_compra.html", form=form)
            areas.append((area_obj, area["monto"]))
            monto += area["monto"]
        for empleado in form.empleados.data:
            empleado_obj = conseguir_empleado_de_id(empleado["id_empleado"])
            if empleado["monto"] > empleado_obj.importe:
                flash("El monto de un empleado no puede ser superior a su saldo", "danger")
                return render_template("compras/creacion_compra.html", form=form)
            empleados.append((empleado_obj, empleado["monto"]))
            monto += empleado["monto"]
        for fondo in form.fondos.data:
            fondo_obj = conseguir_fondo_de_id(fondo["titulo_fondo"])
            if fondo["monto"] > fondo_obj.saldo:
                flash("El monto de un fondo no puede ser superior a su saldo", "danger")
                return render_template("compras/creacion_compra.html", form=form)
            fondos.append((fondo_obj, fondo["monto"]))
            monto += fondo["monto"]
        if (form.estado.data == "APROBADA" and monto <= form.importe.data) or (form.estado.data == "REALIZADA" and monto == form.importe.data):
            crear_compra(
                form.fecha.data, form.descripcion.data, form.proveedor.data,
                form.solicitante.data, form.importe.data, form.observaciones.data,
                form.estado.data, form.numero_factura.data, fondos, empleados, areas
            )
            flash("Compra agregada correctamente", "success")
        elif form.estado.data not in ["APROBADA", "REALIZADA"]:
            crear_compra(
                form.fecha.data, form.descripcion.data, form.proveedor.data,
                form.solicitante.data, form.importe.data, form.observaciones.data,
                form.estado.data, form.numero_factura.data, [], [], []
            )
            flash("Compra agregada correctamente", "success")
        else:
            print("Entro al else")
            flash("El monto de las áreas, empleados y fondos no coincide con el importe de la compra", "danger")
            return render_template("compras/creacion_compra.html", form=form)
        
        return redirect(url_for("compra.lista_compras"))
    else:
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]
        flash(
            f"Error en el campo {getattr(form, first_error_field).label.text}: {first_error_message}",
            "danger",
        )
        return render_template("compras/creacion_compra.html", form=form)

@bp.get("/editar_compra/<int:id_compra>")
@role_required('Administrador', 'Colaborador')
def editar_compra(id_compra):
    return render_template("compras/paso.html")

@bp.post("/editando_compra/<int:id_compra>")
@role_required('Administrador', 'Colaborador')
def editando_compra(id_compra):
    return render_template("compras/paso.html")



