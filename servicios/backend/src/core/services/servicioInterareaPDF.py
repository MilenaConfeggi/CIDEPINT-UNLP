from io import BytesIO
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from servicios.backend.src.core.services.servicioInterarea import generarNroInterarea
from documentos.Interareas.PDF_TEMPLATES import PDF_TEMPLATES
import os

def generar_pdf(data):
    output_file_path = None  # Inicializar la variable
    try:
        buffer = BytesIO()
        c = canvas.Canvas(buffer)

        pdf_base = PDF_TEMPLATES.get(data.get("tipo"), {}).get("path")

        # Rellenar campos del PDF
        fields = PDF_TEMPLATES[data.get("tipo")]["fields"]
        for field_name, field_info in fields.items():
            c.setFont("Helvetica", field_info["size"])
            value = data.get(field_name, "")
            if not isinstance(value, str):  # Convertir valores no textuales a cadena
                value = str(value)
            c.drawString(field_info["x"], field_info["y"], value)
        
        c.save()
        buffer.seek(0)

        # Combinar el PDF base con el PDF generado
        reader = PdfReader(pdf_base)
        writer = PdfWriter()

        overlay_pdf = PdfReader(buffer)
        for page in reader.pages:
            page.merge_page(overlay_pdf.pages[0])
            writer.add_page(page)

        # Crear el nombre del archivo de salida
        tipo = data.get("tipo")
        identificacion = generarNroInterarea()
        fecha = datetime.now().strftime("%Y/%m/%d")
        output_file_name = f"{tipo}_{identificacion}.pdf"
        output_file_path = os.path.join("documentos/interareas/solicitudes", output_file_name)

        # Guardar el PDF final
        os.makedirs("documentos/interareas/solicitudes", exist_ok=True)
        with open(output_file_path, "wb") as output_file:
            writer.write(output_file)
    except Exception as e:
        print(f"Error en servicio interarea: {str(e)}")

    return output_file_name  # Devuelve None si ocurrió un error