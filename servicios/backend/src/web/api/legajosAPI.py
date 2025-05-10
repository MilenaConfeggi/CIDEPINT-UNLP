from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask import current_app as app
from models.legajos import (
    list_legajos,
    find_legajo_by_id,
    create_legajo,
    list_legajos_all,

)
from models.clientes import find_cliente_by_cuit
from models.documentos import find_estado_by_nombre, get_documento
from models.clientes import create_cliente
from ..schemas.legajos import legajos_schema, legajo_schema, pagination_legajos_schema
from ..schemas.cliente import cliente_schema
from models.base import db
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os
from pathlib import Path
from servicios.backend.src.core.config import config
from servicios.backend.src.web.helpers.auth import check_permission
from flask_jwt_extended import jwt_required
from models.distribucion import Distribucion
from models.mails.mail import Mail
from models.muestras.muestra import Muestra
from models.presupuestos.presupuesto import Presupuesto
from models.documentos.documento import Documento
from models.legajos.legajo import Legajo

bp = Blueprint("legajos", __name__, url_prefix="/api/legajos")


@bp.get("/")
@jwt_required()
def listar_legajos():
    if not check_permission("listar_legajos"):
        return jsonify({"message": "No tiene permiso para acceder a este recurso"}), 403
    params = request.args
    empresa = params.get("empresa", "")
    fecha = params.get("fecha", "")
    area = params.get("area", "")
    ensayo = params.get("ensayo", "")
    page = params.get("page", 1, int)
    per_page = params.get("per_page", 10, int)
    pagination = list_legajos(
        page=page,
        per_page=per_page,
        empresa=empresa,
        fecha=fecha,
        area=area,
        ensayo=ensayo,
    )
    result = pagination_legajos_schema.dump(pagination)
    return jsonify(result), 200


@bp.get("/<string:id>")
def get_legajo(id):
    if not check_permission("ver_legajo"):
        return jsonify({"message": "No tiene permiso para acceder a este recurso"}), 403
    data = legajo_schema.dump(find_legajo_by_id(id))
    if data is None:
        return jsonify({"error": "No se encontro el legajo"}), 404
    return jsonify(data), 200


@bp.post("/add")
def add_legajo():
    if not check_permission("crear_legajo"):
        return jsonify({"message": "No tiene permiso para acceder a este recurso"}), 403
    data = request.get_json()
    legajo = create_legajo(data.get("legajo"))
    if legajo is None:
        return jsonify({"error": "No se pudo crear el legajo"}), 400
    cliente = create_cliente(data.get("cliente"), legajo.id)
    if cliente is None:
        return jsonify({"error": "Ya existe un cliente con ese email"}), 400
    return jsonify({"message": "Legajo creado"}), 201


@bp.post("/cancel/<int:id>")
def cancel_legajo(id):
    motivo = request.get_json().get("motivo")
    proc = request.get_json().get("proc")
    legajo = find_legajo_by_id(id)
    if legajo is None:
        return jsonify({"error": "No se encontro el legajo"}), 404
    legajo.estado = find_estado_by_nombre("Cancelado")
    legajo.motivo_cancelacion = motivo
    legajo.parte_del_proceso_cancelado = proc
    db.session.commit()
    return jsonify({"message": "Legajo cancelado"}), 200

@bp.post("/admin/<int:id>")
def admin_legajo(id):
    legajo = find_legajo_by_id(id)
    if legajo is None:
        return jsonify({"error": "No se encontro el legajo"}), 404
    legajo.admin_habilitado = True
    db.session.commit()
    return jsonify({"message": "Legajo habilitado"}), 200

@bp.get("/all")
def listado_completo():
    legajos = list_legajos_all()
    data = legajos_schema.dump(legajos)
    return jsonify(data), 200

@bp.post("/mandar_informe")
def enviar_correo_con_link_y_pdf():
    mail = request.get_json().get("mail")
    link = request.get_json().get("link")
    legajo_id = request.get_json().get("legajo_id")
    doc_id = request.get_json().get("arch")
    doc = get_documento(doc_id)
    if doc is None:
        return jsonify({"error": "No se encontro el documento"}), 404
    
    
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[5]
    documentos_path = project_root / "documentos" / "informes" / str(legajo_id)
    file_path = documentos_path / doc.nombre_documento
    try:
        # Configuración del servidor SMTP
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(config["development"].MAIL_USER, config["development"].MAIL_PASSWORD)
        
        # Crear el mensaje
        msg = MIMEMultipart()
        msg["From"] = config["development"].MAIL_USER
        msg["To"] = mail
        msg["Subject"] = "Correo con enlace y archivo adjunto"

        # Cuerpo del mensaje con un enlace
        body = f"""
        Buen día,

        Gracias por hacer uso de nuestro servicio!. A continuación, puede acceder a la siguiente encuesta para poder darnos un feedback: 
        {link}

        Además hemos adjuntado, en formato PDF, el Informe.

        Saludos,
        Equipo CIDEPINT
        """
        msg.attach(MIMEText(body, 'plain'))

        # Adjuntar el archivo PDF
        if os.path.exists(file_path):
            with open(file_path, "rb") as adjunto:
                parte_adjunto = MIMEBase('application', 'octet-stream')
                parte_adjunto.set_payload(adjunto.read())
                encoders.encode_base64(parte_adjunto)
                parte_adjunto.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(file_path)}'
                )
                msg.attach(parte_adjunto)
        else:
            return jsonify({"error": "El archivo PDF no existe en la ruta especificada"}), 500

        # Enviar el correo
        servidor.sendmail(config["development"].MAIL_USER, mail, msg.as_string())
        servidor.quit()
        return jsonify({"message": "Correo enviado con exito"}), 200
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return jsonify({"error": "Error al enviar el correo"}), 500

@bp.get("/validar-cuit/<string:cuit>")
@jwt_required()
def validar_cuit(cuit):
    cliente = find_cliente_by_cuit(cuit)
    if cliente is None:
        return jsonify({"error": "No se encontro el cliente"}), 404
    data = cliente_schema.dump(cliente)
    return jsonify(data), 200

@bp.post("/delete/<int:id>")
def delete_legajo(id):
    legajo = find_legajo_by_id(id)
    if legajo is None:
        return jsonify({"error": "No se encontró el legajo"}), 404

    try:
        # Eliminar dependencias relacionadas manualmente en el orden correcto
        # 1. Eliminar registros relacionados en empleado_distribucion
        db.session.execute(
            text("DELETE FROM empleado_distribucion WHERE distribucion_id IN (SELECT id FROM distribucion WHERE legajo_id = :legajo_id)"),
            {"legajo_id": id}
        )

        # 2. Eliminar registros relacionados en presupuesto_stan
        db.session.execute(
            text("DELETE FROM presupuesto_stan WHERE presupuesto_id IN (SELECT id FROM presupuesto WHERE legajo_id = :legajo_id)"),
            {"legajo_id": id}
        )

        # 3. Eliminar registros relacionados en presupuesto
        db.session.query(Presupuesto).filter_by(legajo_id=id).delete()

        # 4. Eliminar registros relacionados en distribucion
        db.session.query(Distribucion).filter_by(legajo_id=id).delete()

        # 5. Eliminar otras dependencias
        db.session.query(Mail).filter_by(legajo_id=id).delete()
        db.session.query(Muestra).filter_by(legajo_id=id).delete()
        db.session.query(Documento).filter_by(legajo_id=id).delete()

        # 6. Finalmente, eliminar el legajo
        db.session.delete(legajo)
        db.session.commit()
        return jsonify({"message": "Legajo eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar el legajo: {e}")
        return jsonify({"error": f"Error al eliminar el legajo: {str(e)}"}), 500
    
@bp.get("/next-id")
def get_next_legajo_id():
    last_legajo = db.session.query(Legajo).order_by(Legajo.id.desc()).first()
    next_id = last_legajo.id + 1 if last_legajo else 1  # Si no hay legajos, el próximo ID será 1
    return jsonify({"next_id": next_id}), 200