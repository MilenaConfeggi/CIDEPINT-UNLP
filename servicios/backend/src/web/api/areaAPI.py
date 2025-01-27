from flask import Blueprint, request, jsonify
from flask import current_app as app
from models.personal.area import Area
from models.base import db
from ..schemas.area import area_schema, area_schemas
from flask import Blueprint, request, jsonify
from flask import current_app as app
from datetime import datetime
from models.personal import list_areas
from servicios.backend.src.web.helpers.auth import is_authenticated, check_permission
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('area', __name__, url_prefix='/api/area')

@bp.get('/')
@jwt_required()
def listar_areas():
    if not check_permission("listar_areas"):
        return jsonify({"message": "No tiene permiso para acceder a este recurso"}), 403
    data = area_schemas.dump(list_areas())
    return jsonify(data), 200