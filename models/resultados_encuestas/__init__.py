from .resultado_encuesta import ResultadoEncuesta


def create_resultado_encuesta(key):
    if key is None:
        return None
    encuesta = ResultadoEncuesta(
        unique_key=key,
    )
    return encuesta

def find_resultado_encuesta_by_id(id):
    return ResultadoEncuesta.query.filter_by(id=id).first()

def find_resultado_encuesta_by_unique_key(unique_key):
    return ResultadoEncuesta.query.filter_by(unique_key=unique_key).first()

def cant_conformidad(puntuacion):
    return ResultadoEncuesta.query.filter_by(calificacion_general=puntuacion).count()

