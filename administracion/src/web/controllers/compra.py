from flask import Blueprint, render_template, request, redirect, flash, url_for, Response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from flask_login import current_user
from administracion.src.core.compras.compra import filtrar_compras, buscar_compra, filtrar_compras_descargadas, crear_compra, borrar_compra, agregar_fuentes_a_compra, obtener_fondos, obtener_areas, obtener_empleados, editar_compra_espera, editar_compra_aprobada_o_realizada, realizar_compra_aprobada
from administracion.src.core.proveedores.proveedor import filtrar_proveedores, chequeo_razon_social_existente, crear_proveedor, borrar_proveedor, actualizar_proveedor, buscar_proveedor
from administracion.src.web.forms.form_agregar_proveedor import form_agregar_proveedor
from administracion.src.web.forms.form_editar_proveedor import form_editar_proveedor
from administracion.src.web.forms.form_agregar_compra import form_agregar_compra
from administracion.src.web.forms.form_editar_compra import form_editar_compra
from administracion.src.web.forms.form_aprobar_compra import form_aprobar_compra
from administracion.src.web.forms.form_realizar_compra import form_realizar_compra
from administracion.src.web.controllers.roles import role_required
from administracion.src.core.servicios.personal import listar_empleados, listar_areas, conseguir_area_de_id, conseguir_empleado_de_id
from administracion.src.core.fondos.fondo import listar_fondos, conseguir_fondo_de_id

bp = Blueprint("compra",__name__,url_prefix="/compra")

@bp.get("/")
@role_required('Administrador', 'Colaborador', 'Personal') 
def index():
    return render_template("compras/inicio.html", rol=current_user.rol)

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
                "La razon social ingresada ya se encuentra registrada en el sistema", "error"
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
            "error",
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
        flash("Proveedor no encontrado", "error")
        return redirect(url_for("compra.lista_proveedores"))
    form = form_editar_proveedor(request.form, obj=proveedor)
    if form.validate_on_submit():
        razon_social = form.razon_social.data
        contacto = form.contacto.data
        if razon_social != proveedor.razon_social and chequeo_razon_social_existente(form.razon_social.data):
            flash(
                "La razon social ingresada ya se encuentra registrada en el sistema", "error"
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
            "error",
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
        fecha_menor, fecha_mayor, estado, current_user.rol, current_user.empleado.area_id, page, per_page
    )
    return render_template("compras/listado_compras.html", compras=compras, rol=current_user.rol) 

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
        fecha_menor, fecha_mayor, estado, current_user.rol, current_user.empleado.area_id
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
        fecha_menor, fecha_mayor, estado, current_user.rol, current_user.empleado.area_id
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

class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

def validar_montos_y_acumular(form):
    monto = 0
    fondos, empleados, areas = [], [], []
    
    for area in form.areas.data:
        area_obj = conseguir_area_de_id(area["id_area"])
        if area["monto"] > area_obj.saldo:
            raise ValidationError("El monto de un área no puede ser superior a su saldo")
        areas.append((area_obj, area["monto"]))
        monto += area["monto"]

    for empleado in form.empleados.data:
        empleado_obj = conseguir_empleado_de_id(empleado["id_empleado"])
        if empleado["monto"] > empleado_obj.saldo:
            raise ValidationError("El monto de un empleado no puede ser superior a su saldo")
        empleados.append((empleado_obj, empleado["monto"]))
        monto += empleado["monto"]
    
    for fondo in form.fondos.data:
        fondo_obj = conseguir_fondo_de_id(fondo["id_fondo"])
        if fondo["monto"] > fondo_obj.saldo:
            raise ValidationError("El monto de un fondo no puede ser superior a su saldo")
        fondos.append((fondo_obj, fondo["monto"]))
        monto += fondo["monto"]

    return monto, areas, empleados, fondos

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
    lista_areas = listar_areas()
    lista_empleados = listar_empleados()
    lista_fondos = listar_fondos()
    if form.validate_on_submit():
        try:
            monto, areas, empleados, fondos = validar_montos_y_acumular(form)
        except ValidationError as e:
            flash("Compra no agregada", "error")
            return render_template("compras/creacion_compra.html", form=form, areas=lista_areas, empleados=lista_empleados, fondos=lista_fondos)
        if (form.estado.data == "APROBADA" and monto <= form.importe.data) or (form.estado.data == "REALIZADA" and monto <= form.importe.data):
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
            flash("El monto de las áreas, empleados y fondos no coincide con el importe de la compra", "error")
            return render_template("compras/creacion_compra.html", form=form, areas=lista_areas, empleados=lista_empleados, fondos=lista_fondos)
        
        return redirect(url_for("compra.lista_compras"))
    else:
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]
        flash(
            f"Error en el campo {getattr(form, first_error_field).label.text}: {
              first_error_message}",
            "error",
        )
        return render_template("compras/creacion_compra.html", form=form, areas=lista_areas, empleados=lista_empleados, fondos=lista_fondos)

@bp.get("/editar_compra/<int:id_compra>")
@role_required('Administrador', 'Colaborador')
def editar_compra(id_compra):
    areas = listar_areas()
    empleados = listar_empleados()
    fondos = listar_fondos()
    compra = buscar_compra(id_compra)
    if not compra:
        return redirect(url_for("compra.lista_compras"))
    form = form_editar_compra(obj=compra)
    form.fondos.entries = []
    form.areas.entries = []
    form.empleados.entries = []
    for fondo in obtener_fondos(id_compra):
        form.fondos.append_entry({'id_fondo': fondo.fondo_id, 'monto': fondo.contribucion})
    for area in obtener_areas(id_compra):
        form.areas.append_entry({'id_area': area.area_id, 'monto': area.contribucion})
    for empleado in obtener_empleados(id_compra):
        form.empleados.append_entry({'id_empleado': empleado.empleado_id, 'monto': empleado.contribucion})
    return render_template("compras/edicion_compra.html", form=form, compra=compra, areas=areas, empleados=empleados, fondos=fondos)

@bp.post("/editando_compra/<int:id_compra>")
@role_required('Administrador', 'Colaborador')
def editando_compra(id_compra):
    form = form_editar_compra(request.form)
    lista_areas = listar_areas()
    lista_empleados = listar_empleados()
    lista_fondos = listar_fondos()
    compra = buscar_compra(id_compra)
    if not compra:
        return redirect(url_for('compra.lista_compras'))
    if form.validate_on_submit():
        try:
            monto, areas, empleados, fondos = validar_montos_y_acumular(form)
        except ValidationError as e:
            flash(e.message, "error")
            return render_template("compras/edicion_compra.html", form=form, compra=compra, areas=lista_areas, empleados=lista_empleados, fondos=lista_fondos)
        if (form.estado.data == "APROBADA" and monto <= form.importe.data) or (form.estado.data == "REALIZADA" and monto <= form.importe.data):
            editar_compra_aprobada_o_realizada(
                compra,
                form.fecha.data, form.descripcion.data, form.proveedor.data,
                form.solicitante.data, form.importe.data, form.observaciones.data,
                form.estado.data, form.numero_factura.data, fondos, empleados, areas
            )
            flash("Compra editada correctamente", "success")
        elif form.estado.data not in ["APROBADA", "REALIZADA"]:
            editar_compra_espera(
                compra,
                form.fecha.data, form.descripcion.data, form.proveedor.data,
                form.solicitante.data, form.importe.data, form.observaciones.data,
                form.estado.data, form.numero_factura.data
            )
            flash("Compra editada correctamente", "success")
        else:
            flash("El monto de las áreas, empleados y fondos no coincide con el importe de la compra", "error")
            return render_template("compras/edicion_compra.html", form=form, compra=compra, areas=lista_areas, empleados=lista_empleados, fondos=lista_fondos)
        
        return redirect(url_for("compra.lista_compras"))
    else:
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]
        flash(
            f"Error en el campo {getattr(form, first_error_field).label.text}: {
              first_error_message}",
            "error",
        )
        return render_template("compras/edicion_compra.html", form=form, compra=compra, areas=lista_areas, empleados=lista_empleados, fondos=lista_fondos)


@bp.get("/aprobar_compra/<int:id_compra>")
@role_required('Administrador', 'Colaborador')
def aprobar_compra(id_compra):
    form = form_aprobar_compra()
    compra = buscar_compra(id_compra)
    if not compra:
        return redirect(url_for('compra.lista_compras'))
    areas = listar_areas()
    empleados = listar_empleados()
    fondos = listar_fondos()
    return render_template("compras/aprobar_compra.html", form=form, compra=compra, areas=areas, empleados=empleados, fondos=fondos)

@bp.post("/aprobando_compra/<int:id_compra>")
@role_required('Administrador', 'Colaborador')
def aprobando_compra(id_compra):
    form = form_aprobar_compra(request.form)
    lista_areas = listar_areas()
    lista_empleados = listar_empleados()
    lista_fondos = listar_fondos()
    compra = buscar_compra(id_compra)
    if not compra:
        flash("Compra no encontrada", "error")
        return redirect(url_for("compra.lista_compras"))
    if form.validate_on_submit():
        try:
            monto, areas, empleados, fondos = validar_montos_y_acumular(form)
        except ValidationError as e:
            flash(e.message, "error")
            return render_template("compras/aprobar_compra.html", form=form, compra=compra, areas=lista_areas, empleados=lista_empleados, fondos=lista_fondos)
        if (monto <= compra.importe):
            agregar_fuentes_a_compra(
                compra, fondos, empleados, areas
            )
            flash("Compra editada correctamente", "success")
            return redirect(url_for("compra.lista_compras"))
        else:
            flash("El monto de las áreas, empleados y fondos no coincide con el importe de la compra", "error")
            return render_template("compras/aprobar_compra.html", form=form, compra=compra, areas=lista_areas, empleados=lista_empleados, fondos=lista_fondos)
    else:
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0]
        flash(
            f"Error en el campo {getattr(form, first_error_field).label.text}: {
              first_error_message}",
            "error",
        )
        return render_template("compras/aprobar_compra.html", form=form, compra=compra, areas=areas, empleados=empleados, fondos=fondos)

@bp.get("/realizar_compra/<int:id_compra>")
@role_required('Administrador', 'Colaborador')
def realizar_compra(id_compra):
    compra = buscar_compra(id_compra)
    if not compra:
        return redirect(url_for('compra.lista_compras'))
    form = form_realizar_compra(obj=compra)
    form.fondos.entries = []
    form.areas.entries = []
    form.empleados.entries = []
    for fondo in obtener_fondos(id_compra):
        form.fondos.append_entry({'id_fondo': fondo.fondo_id, 'monto': fondo.contribucion})
    for area in obtener_areas(id_compra):
        form.areas.append_entry({'id_area': area.area_id, 'monto': area.contribucion})
    for empleado in obtener_empleados(id_compra):
        form.empleados.append_entry({'id_empleado': empleado.empleado_id, 'monto': empleado.contribucion})
    compra = buscar_compra(id_compra)
    areas = listar_areas()
    empleados = listar_empleados()
    fondos = listar_fondos()
    return render_template("compras/realizar_compra.html", form=form, compra=compra, areas=areas, empleados=empleados, fondos=fondos)

@bp.post("/realizando_compra/<int:id_compra>")
@role_required('Administrador', 'Colaborador')
def realizando_compra(id_compra):
    form = form_realizar_compra(request.form)
    lista_areas = listar_areas()
    lista_empleados = listar_empleados()
    lista_fondos = listar_fondos()
    compra = buscar_compra(id_compra)
    if not compra:
        flash("Compra no encontrada", "error")
        return redirect(url_for("compra.lista_compras"))
    if form.validate_on_submit():
        try:
            monto, areas, empleados, fondos = validar_montos_y_acumular(form)
        except ValidationError as e:
            flash(e.message, "error")
            return render_template("compras/realizar_compra.html", form=form, compra=compra, areas=lista_areas, empleados=lista_empleados, fondos=lista_fondos)
        if (monto <= compra.importe):
            realizar_compra_aprobada(
                compra, fondos, empleados, areas
            )
            flash("Compra realizada correctamente", "success")
            return redirect(url_for("compra.lista_compras"))
        else:
            flash("El monto de las áreas, empleados y fondos no coincide con el importe de la compra", "error")
            return render_template("compras/realizar_compra.html", form=form, compra=compra, areas=lista_areas, empleados=lista_empleados, fondos=lista_fondos)
    else:
        first_error_field = next(iter(form.errors))
        first_error_message = form.errors[first_error_field][0] 
        flash(
            f"Error en el campo {getattr(form, first_error_field).label.text}: {
              first_error_message}",
            "error",
        )
        return render_template("compras/aprobar_compra.html", form=form, compra=compra, areas=areas, empleados=empleados, fondos=fondos) 

@bp.get("/rechazar_compra/<int:id_compra>")
@role_required('Administrador', 'Colaborador')
def rechazar_compra(id_compra):
    compra = buscar_compra(id_compra)
    if not compra:
        return redirect(url_for('compra.lista_compras'))
    return render_template("compras/rechazar_compra.html", compra=compra)

@bp.post("/rechazando_compra/<int:id_compra>")
@role_required('Administrador', 'Colaborador')
def rechazando_compra(id_compra):
    compra = buscar_compra(id_compra)
    if not compra:
        flash("Compra no encontrada", "error")
        return redirect(url_for("compra.lista_compras"))

    motivo_rechazo = request.form.get("opciones")
    otro_motivo = request.form.get("customReason")
    if otro_motivo and motivo_rechazo == "Otros":
        motivo_rechazo = otro_motivo

    borrar_compra(compra, motivo_rechazo)

    flash(f"Compra rechazada por el siguiente motivo: {motivo_rechazo}", "success")
    return redirect(url_for("compra.lista_compras"))