from servicios.backend.src.core.services.servicioInterarea import crear_estadoInterarea

def seeds_estados():
    estados_data = [
        {
            "nombre": "Cargado"
        },
        {
            "nombre": "Firmado"
        },
        {
            "nombre": "Resuelto"
        }
    ]
    for data in estados_data:
        crear_estadoInterarea(data.get("nombre"))