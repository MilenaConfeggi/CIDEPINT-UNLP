from io import BytesIO
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from servicios.backend.src.core.services.servicioInterarea import generarNroInterarea
from documentos.Interareas.PDF_TEMPLATES import PDF_TEMPLATES
import os
import io

def generar_pdf(data):
    output_file_path = None  
    try:
        buffer = BytesIO()
        c = canvas.Canvas(buffer)

        pdf_base = PDF_TEMPLATES.get(data.get("tipo"), {}).get("path")

        # Rellenar campos del PDF
        fields = PDF_TEMPLATES[data.get("tipo")]["fields"]
        for field_name, field_info in fields.items():
            c.setFont("Helvetica", field_info["size"])
            value = data.get(field_name, "")
            if not isinstance(value, str):  
                value = str(value)
            c.drawString(field_info["x"], field_info["y"], value)
        
        c.save()
        buffer.seek(0)

        reader = PdfReader(pdf_base)
        writer = PdfWriter()

        overlay_pdf = PdfReader(buffer)
        for page in reader.pages:
            page.merge_page(overlay_pdf.pages[0])
            writer.add_page(page)

        tipo = data.get("tipo")
        identificacion = generarNroInterarea()
        output_file_name = f"{tipo}_{identificacion}.pdf"
        output_file_path = os.path.join("documentos/interareas/solicitudes", output_file_name)

        os.makedirs("documentos/interareas/solicitudes", exist_ok=True)
        with open(output_file_path, "wb") as output_file:
            writer.write(output_file)
    except Exception as e:
        print(f"Error en servicio interarea: {str(e)}")
    return output_file_name  # Devuelve None si ocurrió un error

def descargar_solicitud(file_name):
    try:
        file_path = f"documentos/interareas/solicitudes/{file_name}"
        with open(file_path, "rb") as file:
            file_content = file.read()
            file_stream = io.BytesIO(file_content)
            file_stream.seek(0) 
            return file_stream
    except Exception as e:
        print(f"Error en servicio interarea: {str(e)}")
        return None

def subir_archivo_completo(file, file_name):
    try:
        # Definir la ruta completa del archivo
        file_path = os.path.join("documentos/interareas/solicitudes", file_name)
        
        # Guardar el archivo en la ruta especificada
        file.save(file_path)

        return file_path
    except Exception as e:
        print(f"Error en servicio interarea: {str(e)}")
        return None

def subir_archivo_firmado(file, file_name):
    try:
        # Obtener el nombre base del archivo sin la extensión
        base_name, ext = os.path.splitext(file_name)
        
        # Crear el nuevo nombre del archivo agregando "firmado" al final
        new_file_name = f"{base_name}_firmado{ext}"
        
        # Definir la ruta completa del archivo original y el nuevo archivo
        original_file_path = os.path.join("documentos/interareas/solicitudes", file_name)
        new_file_path = os.path.join("documentos/interareas/solicitudes", new_file_name)
        
        # Renombrar el archivo original
        if os.path.exists(original_file_path):
            os.rename(original_file_path, new_file_path)
        
        # Guardar el nuevo archivo en la ruta especificada
        file.save(new_file_path)

        return new_file_path
    except Exception as e:
        print(f"Error en servicio interarea: {str(e)}")
        return None