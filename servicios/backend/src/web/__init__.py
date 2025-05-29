from flask import Flask, render_template
from servicios.backend.src.core.config import config
from servicios.backend.src.core.seeds import seedsMuestra
from servicios.backend.src.core.seeds import seedsMails
from servicios.backend.src.core.seeds import seedsCliente
from servicios.backend.src.core.seeds import seedsLegajo
from servicios.backend.src.core.seeds import seedsEstados
from servicios.backend.src.core.seeds import seedsDocumento
from servicios.backend.src.core.seeds import seedsArea
from servicios.backend.src.core.seeds import seedsUsuario
from servicios.backend.src.core.seeds import seedsStans
from servicios.backend.src.core.seeds import seedsInterarea
from servicios.backend.src.core.seeds import seedsEstadoInterarea
from servicios.backend.src.core.seeds import seedsCertificado
from servicios.backend.src.core.seeds import seedsPresupuesto
from servicios.backend.src.core.seeds import seedsMedioPago
from models import db
from servicios.backend.src.web.controllers.mails import bp as mails_bp
from servicios.backend.src.web.controllers.muestras import bp as muestras_bp
from servicios.backend.src.web.controllers.informes import bp as informes_bp
from servicios.backend.src.web.controllers.usuarios import bp as usuarios_bp
from servicios.backend.src.web.controllers.auth import bp as auth_bp
from servicios.backend.src.web.controllers.stans import bp as stans_bp
from servicios.backend.src.web.api.legajosAPI import bp as legajos_api_bp
from servicios.backend.src.web.api.documentoAPI import bp as documentos_api_bp
from servicios.backend.src.web.controllers.interarea import bp as interarea_bp
from servicios.backend.src.web.api.areaAPI import bp as area_bp
from servicios.backend.src.web.controllers.certificado import bp as certificado_bp
from servicios.backend.src.web.api.encuesta import bp as encuestas_bp
from servicios.backend.src.web.controllers.presupuesto import bp as presupuesto_bp
from servicios.backend.src.web.controllers.estadisticas import bp as estadisticas
from servicios.backend.src.web.controllers.frontend_routes import frontend_bp
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()


def create_app(env="development", static_folder=""):
    app = Flask(__name__)
    app.config.from_object(config[env])
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 6 * 3600 #El token de autenticación caducará en 6 horas
    app.url_map.strict_slashes = False
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
    app.register_blueprint(interarea_bp)
    app.register_blueprint(certificado_bp)
    app.register_blueprint(encuestas_bp)
    app.register_blueprint(presupuesto_bp)
    app.register_blueprint(estadisticas)
    app.register_blueprint(frontend_bp)

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
        seedsMedioPago.seeds_medio_pago()
        print("Medios de pago creados!")
        seedsArea.seeds_areas()
        print("Areas creados!")
        seedsEstados.seeds_estados()
        print("Estados creados!")
        seedsDocumento.seeds_tipos_documento()
        print("Tipos de documentos creados!")
        seedsStans.seeds_stans()
        print("Stans creados!")
        seedsLegajo.seeds_legajos()
        print("Legajos creados!")
        seedsMuestra.seeds_muestras()
        print("Muestras creadas!")
        seedsMails.seeds_mails()
        print("Mails creados!")
        seedsUsuario.seeds_usuarios()
        print("Usuarios creados!")
        seedsEstadoInterarea.seeds_estados()
        print("Estados de interareas creados!")
        seedsCliente.seeds_clientes()
        print("Clientes creados!")

    @app.cli.command(name="seeds-finales-db")
    def seeds_finales():
        """
        Comando para crear los seeds de la base de datos que va a ser entregado al CIDEPINT
        """
        seedsMedioPago.seeds_medio_pago()
        print("Medios de pago creados!")
        seedsArea.seeds_areas()
        print("Areas creadas!")
        seedsEstados.seeds_estados()
        print("Estados creados!")
        seedsDocumento.seeds_tipos_documento()
        print("Tipos de documentos creados!")
        seedsStans.seeds_stans()
        print("Stans creados!")
        seedsMuestra.seeds_muestras()
        print("Muestras creadas!")
        seedsEstadoInterarea.seeds_estados()
        print("Estados de interareas creados!")
        seedsUsuario.seeds_usuarios()
        print("Usuarios creados!")

    return app
    
