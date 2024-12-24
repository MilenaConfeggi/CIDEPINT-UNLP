from models import db
from models.presupuestos.STAN import STAN
from models.presupuestos.mediodepago import MedioPago
from models.presupuestos.ensayo import Ensayo
from models.presupuestos.ensayo_stan import EnsayoStan
from models.presupuestos.presupuesto_stan import PresupuestoStan
from models.presupuestos.presupuesto import Presupuesto
from models.presupuestos.mediodepago import MedioPago
from models.legajos.legajo import Legajo
import re
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, Frame
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
from servicios.backend.src.core.services import servicioDocumento


UPLOAD_FOLDER = os.path.abspath("documentos")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        # Crear los elementos del header una sola vez
        self.create_header_elements()

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_header()
            self.draw_page_footer()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def create_header_elements(self):
        # Rutas de los logos
        logo_cic = os.path.join(UPLOAD_FOLDER, "logos", "CIC.png")
        logo_conicet = os.path.join(UPLOAD_FOLDER, "logos", "CONICET.jpg")
        logo_unlp = os.path.join(UPLOAD_FOLDER, "logos", "UNLP.png")
        
        # Crear los elementos de la tabla
        self.image_cic = Image(logo_cic, width=1.2*inch, height=0.6*inch)
        self.image_conicet = Image(logo_conicet, width=1.5*inch, height=0.6*inch)
        self.image_unlp = Image(logo_unlp, width=1.2*inch, height=0.6*inch)
        
        # Crear la tabla de logos
        self.logos_table = Table([[self.image_cic, self.image_conicet, self.image_unlp]])
        self.logos_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

    def draw_page_header(self):
        self.saveState()
        
        # Obtener dimensiones de la página
        width, height = letter
        
        # Frame para el header
        header_frame = Frame(
            72,  # x
            height - 72 - 1.5*inch,  # y
            width - 144,  # width
            1.5*inch,  # height
            leftPadding=0,
            bottomPadding=0,
            rightPadding=0,
            topPadding=0,
        )
        
        # Elementos del header
        story = []
        story.append(self.logos_table)
        
        # Estilo para el título
        title_style = ParagraphStyle(
            'HeaderTitle',
            fontSize=12,
            alignment=1,
            spaceAfter=10
        )
        
        # Agregar título del CIDEPINT
        story.append(Spacer(1, 12))
        story.append(Paragraph(
            "CIDEPINT - Centro de Investigación Tecnológica y Desarrollo en Tecnología de Pinturas",
            title_style
        ))
        
        # Dibujar el header
        header_frame.addFromList(story, self)
        
        # Línea separadora
        self.line(72, height - 72 - 1.5*inch - 5, width - 72, height - 72 - 1.5*inch - 5)
        
        self.restoreState()

    def draw_page_footer(self):
        self.saveState()
        self.line(72, 60, 540, 60)
        self.setFont('Helvetica', 8)
        
        # Obtener el ancho de la página
        width, _ = letter
        
        # Texto del pie de página
        footer_text = "Av. 52 y calle 121, B1900AYB La Plata, Buenos Aires, Argentina -                        Tel.: +54 - (221) 482-11-21"
        footer_text2 = "Web: http://cidepint.ing.unlp.edu.ar     -     Email: direccion@cidepint.ing.unlp.edu.ar / servicios@cidepint.ing.unlp.edu.ar"
        page_num = f"Página {self._pageNumber} de {len(self._saved_page_states)}"
        
        # Calcular las posiciones centradas
        text_width1 = self.stringWidth(footer_text, 'Helvetica', 8)
        text_width2 = self.stringWidth(footer_text2, 'Helvetica', 8)
        text_width_page = self.stringWidth(page_num, 'Helvetica', 8)
        
        x_centered1 = (width - text_width1) / 2
        x_centered2 = (width - text_width2) / 2
        x_centered_page = (width - text_width_page) / 2
        
        # Dibujar texto centrado
        self.drawString(x_centered1, 45, footer_text)
        self.drawString(x_centered2, 35, footer_text2)
        self.drawString(x_centered_page, 25, page_num)
        
        self.restoreState()

def generar_presupuesto(data):
    # Completar con los datos necesarios
    legajo = Legajo.query.filter_by(id=data.get('legajo')).first()
    medioDePago = MedioPago.query.filter_by(id=data.get('medioDePago')).first()
    presupuesto = data.get('presupuesto')

    precio = 0
    estans = []
    estans_presu = []
    cantidades = []
    for dupla in data.get('seleccionados'):
        estan = STAN.query.filter_by(id=dupla.get('id')).first()
        estan_presu = PresupuestoStan.query.filter_by(stan_id=estan.id, presupuesto_id = presupuesto.id).first()
        precio += estan_presu.precio_carga * dupla.get('cantidad')
        estans.append(estan)
        estans_presu.append(estan_presu)
        cantidades.append(dupla.get('cantidad'))

    # Crear la ruta de destino
    certificado_dir = os.path.join(UPLOAD_FOLDER, "presupuestos", str(legajo.id))
    os.makedirs(certificado_dir, exist_ok=True)  # Crear el directorio si no existe
    timestamp = datetime.now().strftime("%Y%m%d")
    output_filename = os.path.join(certificado_dir, f"presupuesto_{timestamp}.pdf")

    styles = getSampleStyleSheet()
    # Configurar el documento
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=186,  # Espacio adicional para el header
        bottomMargin=80  # Espacio adicional para el footer
    )

    # Estilos predefinidos
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=0
    )
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=14,
        alignment=1,
        spaceAfter=5
    )

    derecha_style = ParagraphStyle(
        'DerechaStyle',
        parent=styles['Normal'],
        fontSize=11,
        alignment=2,
    )

    rojo_style = ParagraphStyle(
        'RojoStyle',
        parent=styles['Normal'],
        fontSize=11,
        color='red',
        textColor=colors.red
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        fontName='Helvetica'
    )
    

    chiquito_style = ParagraphStyle(
        'ChiquitoStyle',
        parent=styles['Normal'],
        fontSize=8,
        leading=14,
        fontName='Helvetica'
    )
    
    bold_style = ParagraphStyle(
        'BoldStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        fontName='Helvetica-Bold'
    )
    content = []

    # Referencia y fecha
    content.append(Paragraph(f"Ref.: Leg. Int. N° {legajo.id}", derecha_style))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"LA PLATA, {datetime.now().strftime("%d de %B de %Y")}", derecha_style))
    content.append(Spacer(1, 12))

    # Datos del cliente
    content.append(Paragraph("<b>Señores</b>", normal_style))
    content.append(Paragraph(legajo.cliente.contacto, normal_style))
    content.append(Paragraph(f"<b>Mail:</b> {legajo.cliente.email}", normal_style))
    content.append(Paragraph(f"<b>At.</b> {legajo.cliente.nombre}", normal_style))
    content.append(Spacer(1, 20))
    
    # Número de presupuesto
    content.append(Paragraph(f"<b>PRESUPUESTO Nº {presupuesto.nro_presupuesto}</b>", title_style))
    content.append(Paragraph("Por la realización de los siguientes ensayos:", normal_style))
    content.append(Spacer(1, 12))

    # Ensayos
    total_costo = 0
    i=0
    for stan in estans:
        if estans[i].precio_por_muestra:
            content.append(Paragraph(f"• {estans[i].descripcion} de {cantidades[i]} muestras", normal_style))
        else:
            content.append(Paragraph(f"• {estans[i].descripcion} por {cantidades[i]} horas", normal_style))
        content.append(Paragraph(f"<b>Costo: U$S {estans_presu[i].precio_carga * cantidades[i]}</b>", normal_style))
        content.append(Spacer(1, 6))
        i+=1

    content.append(Spacer(1, 12))
    content.append(Paragraph(f"<b>Costo final del ensayo............................U$S {precio:.2f}.-</b>", bold_style))
    content.append(Spacer(1, 20))

    # Información adicional
    content.append(Paragraph("A efectos impositivos se paga en pesos al valor del dólar billete venta del Banco Nación del día que se emite la factura.", normal_style))
    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Mantenimiento de la oferta:</b> 15 días corridos.", normal_style))
    content.append(Spacer(1, 12))
    content.append(Paragraph('<b>Aceptación del presupuesto:</b> <span color="red">"ORDEN DE COMPRA A NOMBRE DE FUNDACIÓN FACULTAD DE INGENIERIA".</span>', normal_style))
    content.append(Spacer(1, 12))

    # Percepciones
    content.append(Paragraph("<b>Percepciones:</b> ESTA COTIZACIÓN NO INCLUYE EL MONTO CORRESPONDIENTE A LA PERCEPCIÓN DEL IMPUESTO SOBRE LOS INGRESOS BRUTOS DE LA PROVINCIA DE BUENOS AIRES, EL CUAL DEPENDERÁ DE LA SITUACIÓN IMPOSITIVA DE CADA CLIENTE.", normal_style))
    content.append(Spacer(1, 12))

    # Información de pago
    content.append(Paragraph("<b>Facturación y pago:</b> a la recepción de la factura enviada por correo electrónico.", normal_style))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Las posibilidades de pago son:", normal_style))
    content.append(Spacer(1, 6))

    payment_info = """• Transferencia o depósito bancario en BANCO NACION CTA. CTE 163005/45 CBU 0110030320000163005456 ó BANCO GALICIA CTA. CTE. 4916/2 172/3 CBU 0070172920000004916231. En caso de transferencia o depósito bancario enviar comprobante al correo electrónico servicios@cidepint.ing.unlp.edu.ar, sin este comprobante no se podrá imputar el pago."""
    content.append(Paragraph(payment_info, normal_style))
    content.append(Spacer(1, 12))

    # Información legal
    legal_info = """El CIDEPINT pone en conocimiento del Contratante que la FUNDACIÓN DE LA FACULTAD DE INGENIERÍA PARA LA TRANSFERENCIA TECNOLÓGICA Y LA PROMOCIÓN DE EMPRESAS DE BIENES Y SERVICIOS, matrícula N° 13705 de la Dirección de Personas Jurídicas de la Provincia de Buenos Aires, CUIT 30-67798003-2, con domicilio en calle 1 N° 732 de la ciudad de La Plata, provincia de Buenos Aires, administrará los fondos contemplados en el presente presupuesto, en su carácter de UNIDAD DE VINCULACIÓN TECNOLÓGICA (U.V.T.)."""
    content.append(Paragraph(legal_info, normal_style))
    content.append(Spacer(1, 12))

    # Información de entrega
    delivery_info = [
        ("<b>Entrega de informes o muestras:</b> El CIDEPINT entregará el informe en mano o via mail una vez que el/los ensayo/s se encuentren abonados en su totalidad, lo mismo para la entrega de muestras.", normal_style),
        ("<b>Lugar de retiro de informes:</b> Sede CIDEPINT sito en calle 52 / 121 y 122 S/N La Plata.", normal_style),
        ("<b>Retiro de muestras:</b> El cliente podrá solicitar la devolución de la/s muestra/s sobrantes, o los residuos de las ensayadas, en el momento de retirar el informe o bien dentro de los treinta (30) días de salida del mismo. Si transcurrido este plazo el cliente no hizo lugar a dicha solicitud, la Dirección del CIDEPINT podrá disponer el destino final de aquéllas/os.", normal_style),
    ]

    for info in delivery_info:
        content.append(Paragraph(info[0], info[1]))
        content.append(Spacer(1, 12))


    # Nota final
    content.append(Spacer(1, 60))
    content.append(Paragraph("Nota:<b> En caso de aceptarse el presente presupuesto, se recomienda comunicarse con el CIDEPINT con el fin de solicitar información acerca de las condiciones en que debe remitirse el material a ensayar.</b>", chiquito_style))
    
    # Construir el PDF usando el canvas numerado
    doc.build(content, canvasmaker=NumberedCanvas)

    print(f"PDF generado: {output_filename}")

    # Crear el documento en la base de datos
    data = {
        "nombre_documento": "presupuesto.pdf",
        "estado_id": 5,
        "legajo_id": legajo.id,
        "tipo_id": 2
    }
    servicioDocumento.crear_documento(data)

def buscar_stan(id):
    return STAN.query.get(id)
def buscar_legajo(id):
    return Legajo.query.get(id)

def crear_stan(data):
    stan = STAN(
        numero= "STAN " + data.get('numero'),
        precio_pesos=data.get('precio_pesos'),
        precio_dolares=data.get('precio_dolares'),
        precio_por_muestra=data.get('precio_por_muestra'),
        descripcion=data.get('descripcion')
    )

    if validar_numero_stan(stan.numero) == False:
        return None
    
    db.session.add(stan)
    db.session.commit()
    return stan

def validar_numero_stan(numero):
    stan = STAN.query.filter_by(numero=numero).first()
    if stan is not None:
        return False
    return True

def crear_ensayo(nombre):
    ensayos = listar_ensayos()
    for ensayo in ensayos:
        if ensayo.nombre == nombre:
            return ensayo
    ensayo = Ensayo(
        nombre=nombre
    )

    db.session.add(ensayo)
    db.session.commit()
    return ensayo

def crear_ensayo_stan(ensayo_id, stan_id):
    ensayo_stan = EnsayoStan(
        ensayo_id=ensayo_id,
        stan_id=stan_id
    )

    db.session.add(ensayo_stan)
    db.session.commit()

def listar_stans():

    def extract_number(stan):
        match = re.search(r'\d+', stan.numero)
        return int(match.group()) if match else float('inf')

    stans = STAN.query.all()
    stans.sort(key=extract_number)
    return stans

def listar_ensayos():
    return Ensayo.query.all()

def listar_ensayos_para_stan(id_stan):
    ensayos = db.session.query(Ensayo).join(EnsayoStan).filter(EnsayoStan.stan_id == id_stan).all()
    return ensayos

def modificar_precio_stan(id_stan, data):
    stan = STAN.query.get(id_stan)
    stan.precio_pesos = data.get('precio_pesos')
    stan.precio_dolares = data.get('precio_dolares')
    db.session.commit()

def crear_presupuesto(data):
    presupuesto = Presupuesto(
        precio=data.get('precio'),
        legajo=data.get('legajo'),
        medio_de_pago_id=data.get('medio_de_pago_id'),
    )
    db.session.add(presupuesto)
    db.session.commit()
    return presupuesto

def crear_presupuesto_stan(presupuesto, stan_id):
    presupuesto_stan = PresupuestoStan(
        presupuesto_id=presupuesto_id,
        stan_id=stan_id
    )

    db.session.add(presupuesto_stan)
    db.session.commit()
    return presupuesto

def crear_medio_pago(name):
    medio_pago = MedioPago(
        medio_de_pago = name
    )
    db.session.add(medio_pago)
    db.session.commit()
    return medio_pago

def crear_presupuesto_con_stans(data):
    legajo = buscar_legajo(data.get('legajo'))
    presupuesto = Presupuesto(
        precio=-1,
        legajo=legajo,
        medio_de_pago_id=data.get('medioDePago'),
    )
    db.session.add(presupuesto)
    db.session.flush()

    acu=0
    for dupla in data.get('seleccionados'):
        aux = buscar_stan(dupla.get('id')).precio_dolares
        presupuesto_stan = PresupuestoStan(
            presupuesto_id=presupuesto.id,
            stan_id=dupla.get('id'),
            precio_carga = aux,
        )
        acu += aux * dupla.get('cantidad')
        db.session.add(presupuesto_stan)
    presupuesto.precio = acu
    db.session.commit()
    data['presupuesto'] = presupuesto
    generar_presupuesto(data)
    return presupuesto
    
def listar_medios_de_pago():
    return MedioPago.query.all()