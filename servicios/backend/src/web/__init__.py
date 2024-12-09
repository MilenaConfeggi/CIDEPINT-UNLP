from flask import Flask, render_template
from servicios.backend.src.core.config import config
from servicios.backend.src.core.seeds import seedsMuestra
from servicios.backend.src.core.seeds import seedsMails
from servicios.backend.src.core.seeds import seedsCliente
from servicios.backend.src.core.seeds import seedsLegajo
from servicios.backend.src.core.seeds import seedsEstados
from servicios.backend.src.core.seeds import seedsInforme
from servicios.backend.src.core.seeds import seedsDocumento
from servicios.backend.src.core.seeds import seedsArea
from servicios.backend.src.core.seeds import seedsUsuario
from servicios.backend.src.core.seeds import seedsStans
from models import db
from servicios.backend.src.web.controllers.mails import bp as mails_bp
from servicios.backend.src.web.controllers.muestras import bp as muestras_bp
from servicios.backend.src.web.controllers.informes import bp as informes_bp
from servicios.backend.src.web.controllers.usuarios import bp as usuarios_bp
from servicios.backend.src.web.controllers.auth import bp as auth_bp
from servicios.backend.src.web.controllers.stans import bp as stans_bp
from servicios.backend.src.web.api.legajosAPI import bp as legajos_api_bp
from servicios.backend.src.web.api.documentoAPI import bp as documentos_api_bp
from servicios.backend.src.web.api.areaAPI import bp as area_bp
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()


def create_app(env="development", static_folder=""):
    app = Flask(__name__)
    app.config.from_object(config[env])
    db.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)
    CORS(app)
    @app.route("/")
    def home():
        return "SLAY"

    app.register_blueprint(mails_bp)
    app.register_blueprint(muestras_bp)
    app.register_blueprint(informes_bp)
    app.register_blueprint(legajos_api_bp)
    app.register_blueprint(documentos_api_bp)
    app.register_blueprint(area_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(stans_bp)

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
        seedsArea.seeds_areas()
        print("Areas creados!")
        seedsEstados.seeds_estados()
        print("Estados creados!")
        seedsDocumento.seeds_tipos_documento()
        print("Tipos de documentos creados!")
        seedsLegajo.seeds_legajos()
        print("Legajos creados!")
        seedsMuestra.seeds_muestras()
        print("Muestras creadas!")
        seedsMails.seeds_mails()
        print("Mails creados!")
        seedsCliente.seeds_clientes()
        print("Clientes creados!")
        seedsStans.seeds_stans()
        print("Stans creados!")
        seedsUsuario.seeds_usuarios()
        print("Usuarios creados!")
        #seedsDocumento.seeds_documentos()
        #print("Documentos creados!")

    return app
    
