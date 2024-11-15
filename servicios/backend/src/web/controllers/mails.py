from marshmallow import ValidationError
from servicios.backend.src.core.services import servicioMail
from flask import Blueprint, jsonify, request
from servicios.backend.src.web.schemas.mails import mailsSchema, mailSchema
from servicios.backend.src.core.forms.mails import MailForm

bp = Blueprint('mails', __name__, url_prefix='/mails')

@bp.get("/")
def listar_mails():
    mails = servicioMail.listar_mails()
    data = mailsSchema.dump(mails, many=True)

    return jsonify(data), 200

@bp.post("/subir_mail/<int:id>")
def cargar_mail(id):
    if not request.is_json:
        return jsonify({"error": "Invalid input type, expected JSON"}), 400

    try:
        json_data = request.get_json()
        data = mailSchema.load(json_data) 
        servicioMail.crear_mail(data, id)
        return jsonify({"message": "Mail cargado correctamente"}), 200
    except ValidationError as err:
        return jsonify(err.messages), 400