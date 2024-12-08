from flask import Blueprint, request, jsonify
from flask import current_app as app
from models.personal.area import Area
from models.base import db
from ..schemas.area import area_schema, area_schemas
from flask import Blueprint, request, jsonify
from flask import current_app as app
from datetime import datetime
from models.personal import list_areas

bp = Blueprint('area', __name__, url_prefix='/api/area')

@bp.get('/')
def listar_areas():
    data = area_schemas.dump(list_areas())
    return jsonify(data), 200