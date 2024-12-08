from administracion.src.web.controllers.roles import role_required
from flask import render_template, redirect, url_for
from flask_login import current_user
from administracion.src.web.controllers.patrimonio import bp as patrimonio_bp
from administracion.src.web.controllers.archivos_admin import bp as archivos_bp
from administracion.src.web.controllers.contable import bp as contable_bp
from administracion.src.web.controllers.personal.area_controller import area_bp
from administracion.src.web.controllers.personal.personal_controller import personal_bp
from administracion.src.web.controllers.personal.ausencia_controller import ausencia_bp
from administracion.src.web.controllers.auth_controller import auth_bp

def registrar_rutas(app):

    app.register_blueprint(patrimonio_bp)
    app.register_blueprint(archivos_bp)
    app.register_blueprint(contable_bp)
    app.register_blueprint(area_bp)
    app.register_blueprint(personal_bp)
    app.register_blueprint(ausencia_bp)
    app.register_blueprint(auth_bp)
    
    @app.route("/")
    def landing_page():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('home'))
        

    @app.route("/home")
    @role_required('Administrador', 'Colaborador', 'Personal')
    def home():
        return render_template("topicos.html", topico=True)

    return app