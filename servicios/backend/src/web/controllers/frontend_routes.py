from flask import Blueprint, send_from_directory
import os

# Creamos el blueprint del frontend
frontend_bp = Blueprint("frontend", __name__, 
    static_folder="../../../frontend/dist/static", 
    template_folder="../../../frontend/dist")

@frontend_bp.route("/", defaults={"path": ""})
@frontend_bp.route("/<path:path>")
def catch_all(path):
    # Si existe el archivo solicitado (como main.js o estilos.css), lo enviamos
    full_path = os.path.join(frontend_bp.template_folder, path)
    if os.path.exists(full_path):
        return send_from_directory(frontend_bp.template_folder, path)
    # Si no, devolvemos index.html para que Vue lo maneje con su router
    return send_from_directory(frontend_bp.template_folder, "index.html")
