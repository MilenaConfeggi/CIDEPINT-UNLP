from io import BytesIO
from datetime import datetime
from servicios.backend.src.core.services.servicioInterarea import generarNroInterarea, obtener_interarea
from docx import Document   
import os
import io

def generar_solicitud(tipo):
    output_file_name = None  
    try:
        # Ruta de la carpeta de plantillas
        templates_folder = "documentos/interareas/plantillas"
        word_template_path = os.path.join(templates_folder, f"{tipo}.docx")

        if not os.path.exists(word_template_path):
            raise FileNotFoundError("La plantilla de Word no existe")

        # Cargar la plantilla de Word
        doc = Document(word_template_path)

        # Generar el nombre del archivo
        identificacion = generarNroInterarea()
        output_file_name = f"{tipo}_{identificacion}.docx"
        output_file_path = os.path.join("documentos/interareas/solicitudes", output_file_name)

        # Guardar el documento de Word con el nuevo nombre
        os.makedirs("documentos/interareas/solicitudes", exist_ok=True)
        doc.save(output_file_path)

    except Exception as e:
        print(f"Error en servicio interarea: {str(e)}")
        return None

    return output_file_name  # Devuelve la ruta del archivo generado

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

def subir_archivo_completo(file, id):
    try:
        # Definir la ruta completa del archivo
        interarea = obtener_interarea(id)
        file_path = os.path.join("documentos/interareas/solicitudes", interarea.nombre_archivo)
        
        # Guardar el archivo en la ruta especificada
        file.save(file_path)

        return file_path
    except Exception as e:
        print(f"Error en servicio interarea: {str(e)}")
        return None

def subir_archivo_firmado(file, id):
    try:
        interarea = obtener_interarea(id)

        base_name, ext = os.path.splitext(interarea.nombre_archivo)
        
        new_file_name = f"{base_name}_firmado{ext}"
        
        original_file_path = os.path.join("documentos/interareas/solicitudes", interarea.nombre_archivo)
        
        if os.path.exists(original_file_path):
            file.save(original_file_path)
            
            new_file_path = os.path.join("documentos/interareas/solicitudes", new_file_name)
            os.rename(original_file_path, new_file_path)
        
        return new_file_name
    except Exception as e:
        print(f"Error en servicio interarea: {str(e)}")
        return None