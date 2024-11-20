from servicios.backend.src.core.services.servicioDocumento import crear_documento, crear_estado, crear_tipo_documento

def seeds_informe():
    seed_estados()
    seed_tipo()
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

def seed_tipo():
    #Probalemente haya que agregar
    tipos_data = [
        {
            'nombre': 'informe'
        },
        {
            'nombre': 'certificado'
        },
        {
            'nombre': 'presupuestoCi'
        },
        {
            'nombre': "presupuestoCo"
        },
        {
            'nombre': "ordenCompra"
        },
        {
            'nombre': "comrpobantePago"
        },
        {
            'nombre': "factura"
        },

    ]

    for data in tipos_data:
        crear_tipo_documento(data['nombre'])

def seed_documentos():
    documentos_data = [
        {
            'nombre_documento': 'documento1.pdf',
            'estado_id': 1,
            'legajo_id': 1,
            "tipo_id": 1
        },
        {
            'nombre_documento': 'documento2.pdf',
            'estado_id': 2,
            'legajo_id': 1,
            "tipo_id": 1
        },

        {
            'nombre_documento': 'documento3.pdf',
            'estado_id': 3,
            'legajo_id': 2,
            "tipo_id": 1
        }
    ]

    for data in documentos_data:
        crear_documento(data)