from flask import Blueprint, send_from_directory
import os

frontend_bp = Blueprint("frontend", __name__,
    static_folder="../../../frontend/dist/static",  # Archivos estáticos (JS, CSS)
    template_folder="../../../frontend/dist")        # index.html

# Rutas para archivos estáticos
@frontend_bp.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(frontend_bp.static_folder, filename)

# Rutas del frontend (Vue Router)
@frontend_bp.route("/", defaults={"path": ""})
@frontend_bp.route("/<path:path>")
def catch_all(path):
    return send_from_directory(frontend_bp.template_folder, "index.html")
