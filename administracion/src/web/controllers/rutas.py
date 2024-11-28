from flask import render_template
from administracion.src.web.controllers.patrimonio import bp as patrimonio_bp
from administracion.src.web.controllers.contable import bp as contable_bp
def registrar_rutas(app):

    app.register_blueprint(patrimonio_bp)
    app.register_blueprint(contable_bp)
    @app.route("/")
    def landing_page():
        return render_template("landing_page.html")

    @app.route("/home")
    def home():
        return render_template("home.html")

    return app