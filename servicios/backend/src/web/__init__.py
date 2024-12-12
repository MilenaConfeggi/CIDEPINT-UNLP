from flask import Flask, render_template
from servicios.backend.src.core.config import config
from servicios.backend.src.core.seeds import seedsMuestra
from servicios.backend.src.core.seeds import seedsMails
from servicios.backend.src.core.seeds import seedsCliente
from servicios.backend.src.core.seeds import seedsLegajo
from servicios.backend.src.core.seeds import seedsEstados
from servicios.backend.src.core.seeds import seedsInforme
from servicios.backend.src.core.seeds import seedsDocumento
from models import db
from servicios.backend.src.web.controllers.mails import bp as mails_bp
from servicios.backend.src.web.controllers.muestras import bp as muestras_bp
from servicios.backend.src.web.controllers.informes import bp as informes_bp
from servicios.backend.src.web.api.legajosAPI import bp as legajos_api_bp
from servicios.backend.src.web.api.documentoAPI import bp as documentos_api_bp
from flask_cors import CORS

def create_app(env="development", static_folder=""):
    app = Flask(__name__)
    app.config.from_object(config[env])
    db.init_app(app)
    CORS(app)
    @app.route("/")
    def home():
        return "SLAY"

    app.register_blueprint(mails_bp)
    app.register_blueprint(muestras_bp)
    app.register_blueprint(informes_bp)
    app.register_blueprint(legajos_api_bp)
    app.register_blueprint(documentos_api_bp)

    @app.cli.command(name="reset-db")
    def reset_db():
        """
        Comando para resetear la base de datos
        """
        print("Eliminando base de datos en casacada")
        db.drop_all()
        print("Creando base nuevamente")
        db.create_all()
        print("Done!")
   
    @app.cli.command(name="seeds-db")
    def usuarios_roles_seed():
        """
        Comando para crear los seeds de la base de datos
        """
        seedsEstados.seeds_estados()
        print("Estados creados!")
        seedsDocumento.seeds_tipos_documento()
        print("Tipos de documentos creados!")
        seedsLegajo.seeds_legajos()
        print("Legajos creados!")
        #seedsMuestra.seeds_muestras()
        #print("Muestras creadas!")
        #seedsMails.seeds_mails()
        #print("Mails creados!")
        seedsCliente.seeds_clientes()
        print("Clientes creados!")
        seedsDocumento.seeds_documentos()
        print("Documentos creados!")

    return app
    
