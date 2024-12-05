from models.documentos import create_estado

def seeds_estados():
    estados_data = [
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
        }
    ]
    for data in estados_data:
        create_estado(data)
    