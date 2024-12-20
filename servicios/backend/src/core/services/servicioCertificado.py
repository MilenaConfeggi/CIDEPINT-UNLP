from models.base import db
from models.documentos.documento import Documento
from models.legajos.legajo import Legajo
from models.distribucion import Distribucion
from models.distribucion import get_distribucion
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from servicios.backend.src.core.services import servicioDocumento
import os

UPLOAD_FOLDER = os.path.abspath("documentos")

def generar_certificado(id_legajo, empleados):
    # Completar con los datos necesarios
    legajo = Legajo.query.filter_by(id=id_legajo).first()
    cliente = legajo.cliente.nombre
    fecha_desde = legajo.fecha_entrada.strftime("%d/%m/%Y")
    fecha_hasta = datetime.now().strftime("%d/%m/%Y")
    monto = legajo.presupuesto_cidepint[0].precio
    print(legajo.nro_factura)
    if legajo.nro_factura is None:
        factura = ""
    else:
        factura = legajo.nro_factura

    # Obtener los ensayos de los STANs del presupuesto del legajo
    ensayos = []
    descripcion = []
    for presupuesto in legajo.presupuesto_cidepint:
        for stan in presupuesto.stans:
            descripcion.append(stan.descripcion)
            for ensayo in stan.ensayos:
                ensayos.append(ensayo.nombre)
    ensayo_texto = ", ".join(set(ensayos))  
    descripcion = ", ".join(set(descripcion))
    presupuesto = legajo.presupuesto_cidepint[0].nro_presupuesto

    # Crear la ruta de destino
    certificado_dir = os.path.join(UPLOAD_FOLDER, "certificados", str(id_legajo))
    os.makedirs(certificado_dir, exist_ok=True)  # Crear el directorio si no existe
    output_filename = os.path.join(certificado_dir, "certificado.pdf")

    doc = SimpleDocTemplate(output_filename)

    # Estilos predefinidos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,  # Centrado
        spaceAfter=12
    )
    content = []

    # Rutas de los logos
    logo_cic = os.path.join(UPLOAD_FOLDER, "logos", "CIC.png")
    logo_conicet = os.path.join(UPLOAD_FOLDER, "logos", "CONICET.jpg")
    logo_unlp = os.path.join(UPLOAD_FOLDER, "logos", "UNLP.png")

    # Insertar logos
    image_cic = Image(logo_cic, width=1.2*inch, height=0.6*inch)
    image_conicet = Image(logo_conicet, width=1.5*inch, height=0.6*inch)
    image_unlp = Image(logo_unlp, width=1.2*inch, height=0.6*inch)
    logos_table = Table([[image_cic, image_conicet, image_unlp]])
    logos_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))

    # Títulos y párrafos
    content.append(logos_table)
    content.append(Paragraph("CIDEPINT - Centro de Investigación Tecnológica y Desarrollo en Tecnología de Pinturas", title_style))
    content.append(Spacer(1, 12))

    # Texto principal (contenido existente)
    content.append(Paragraph(f"La dirección del CIDEPINT certifica que la actividad tecnológica titulada <b>{ensayo_texto}</b> para <b>{cliente}</b> se ejecutó desde "
                             f"{fecha_desde} al {fecha_hasta}. Conforme a las definiciones de la Gerencia de Vinculación Tecnológica del CONICET y el "
                             "sistema SIGEVA, se tipificó esta actividad como: <b>Servicio</b>", styles["BodyText"]))
    content.append(Spacer(1, 12))  # Espaciador entre párrafos
    content.append(Paragraph("<b>Descripcion de la Actividad Tecnológica.</b>", styles["BodyText"]))
    content.append(Paragraph(f"{descripcion}", styles["BodyText"]))
    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Integrantes del Grupo Ejecutor</b>", styles["BodyText"]))
    content.append(Spacer(1, 6))

    # Agregar la tabla con datos de los integrantes
    datos_tabla = [["Nombre y Apellido", "Función", "% de Participación"]]
    for empleado in empleados:
        datos_tabla.append([empleado["nombre"], empleado["funcion"], empleado["participacion"]])

    # Crear y estilizar la tabla
    tabla_integrantes = Table(datos_tabla, colWidths=[200, 150, 100])
    tabla_integrantes.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#CCCCCC'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), '#FFFFFF'),
    ]))

    # Agregar tabla al contenido
    content.append(tabla_integrantes)
    content.append(Spacer(1, 12))
    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Datos de la Transferencia de Resultados</b>", styles["BodyText"]))
    content.append(Paragraph("<b>Modalidad de vinculación:</b> STAN", styles["BodyText"]))
    content.append(Paragraph("<b>UVT actuante:</b> Fundación de la Facultad de Ingeniería para la Transferencia Tecnológica y la Promoción de Empresas de Bienes y Servicios de la UNLP (Ffi)", styles["BodyText"]))
    content.append(Paragraph(f"<b>Legajo CIDEPINT:</b> {id_legajo}", styles["BodyText"]))
    content.append(Paragraph(f"<b>Presupuesto NRO:</b> {presupuesto}", styles["BodyText"]))
    content.append(Paragraph(f"<b>Monto:</b> U$S{monto}", styles["BodyText"]))
    content.append(Paragraph(f"<b>Factura C NRO:</b> {factura}", styles["BodyText"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"Por razones de confidencialidad no se incluye el Plan de Trabajo completo, información que queda bajo guarda en el Área de Servicios del CIDEPINT. Todas las actuaciones relacionadas a esta actividad tecnológica han sido informadas al CONICET, CICPBA y UNLP, cumpliendo con la normativa vigente establecida por el convenio CONICET-CICPBA-UNLP (suscripto el 21/10/2015 y la adenda suscripta el 31/08/2017). Esta certificación se extiende el día {fecha_hasta} como documentación probatoria de la ejecución de esta actividad tecnológica realizada por el grupo antes mencionado.", styles["BodyText"]))
    content.append(Spacer(1, 10))
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['BodyText'],
        fontSize=8  # Tamaño de letra más pequeño
    )
    content.append(Paragraph(f"Av. 52 y calle 121, B1900AYB La Plata, Buenos Aires, Argentina - Tel.: +54 - (221) 482-11-21 Email: direccion@cidepint.ing.unlp.edu.ar - Web: http://cidepint.ing.unlp.edu.ar", footer_style))

    # Construir el PDF
    doc.build(content)

    print(f"PDF generado: {output_filename}")

    # Crear el documento en la base de datos
    data = {
        "nombre_documento": "certificado.pdf",
        "estado_id": 5,
        "legajo_id": id_legajo,
        "tipo_id": 1
    }
    servicioDocumento.crear_documento(data)


def obtener_empleados(id_legajo):
    distribucion = Distribucion.query.filter_by(legajo_id=id_legajo).first()
    if not distribucion:
        return None
    empleados = distribucion.empleados_asociados
    nombres = []
    for empleado in empleados:
        nombres.append(f"{empleado.empleado.nombre} {empleado.empleado.apellido}")
    return nombres

def obtener_certificado(id_legajo):
    documento = Documento.query.filter_by(legajo_id=id_legajo, tipo_id=1).first()
    if not documento:
        return None
    return documento.nombre_documento

def calcular_suma_participacion(empleados):
    suma = 0
    for empleado in empleados:
        suma += empleado["participacion"]
    return suma

def chequear_solo_responsable(empleados):
    cant = 0
    for empleado in empleados:
        if empleado["funcion"] == "Responsable del equipo":
            cant += 1
    return cant