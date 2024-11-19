from servicios.backend.src.core.services.servicioInforme import crear_documento, crear_estado

def seeds_informe():
    seed_estados()
    seed_documentos()

def seed_estados():
    estados_data = [
        #estados para documentos        
        {
            'nombre': 'documentado'
        },
        {
            'nombre': 'cargado'
        },
        {
            'nombre': 'firmadoJA'
        },
        {
            'nombre': 'firmado'
        },

    ]

    for data in estados_data:
        crear_estado(data['nombre'])

def seed_documentos():
    documentos_data = [
        {
            'nombre_documento': 'documento1',
            'estado_id': 1,
            'legajo_id': 1
        },
        {
            'nombre_documento': 'documento2',
            'estado_id': 2,
            'legajo_id': 1
        },
        {
            'nombre_documento': 'documento3',
            'estado_id': 3,
            'legajo_id': 1
        },
        {
            'nombre_documento': 'documento4',
            'estado_id': 4,
            'legajo_id': 1
        },
        {
            'nombre_documento': 'documento5',
            'estado_id': 2,
            'legajo_id': 1
        }
    ]

    for data in documentos_data:
        crear_documento(data)