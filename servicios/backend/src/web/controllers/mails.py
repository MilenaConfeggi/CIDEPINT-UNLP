from servicios.backend.src.core.services import servicioMail
from flask import Blueprint, jsonify
from servicios.backend.src.web.schemas.mails import mailsSchema

bp = Blueprint('mails', __name__, url_prefix='/mails')

@bp.get("/")
def listar_mails():
    mails = servicioMail.listar_mails()
    data = mailsSchema.dump(mails, many=True)

    return jsonify(data), 200