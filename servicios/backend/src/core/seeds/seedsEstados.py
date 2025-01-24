from models.documentos import create_estado

def seeds_estados():
    estados_data = [
        #Estados de legajos
        {
            'nombre': 'Informado',
        },
        {
            'nombre': 'En curso',
        },
        {
            'nombre': 'Terminado',
        },
        {
            'nombre': 'Cancelado',
        },
        #Estados de documentos
        {
            "nombre": "Cargado"
        },
        {
            "nombre": "Firmado"
        },
        {
            "nombre": "FirmadoJA"
        },
        {
            "nombre": "Documentado"
        },
        {
            "nombre": "Resuelto"
        }

    ]
    for data in estados_data:
        create_estado(data)
    