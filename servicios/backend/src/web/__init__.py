from flask import Flask, render_template
from servicios.backend.src.core.config import config
from servicios.backend.src.core.seeds import seedsMuestra
from servicios.backend.src.core.seeds import seedsMails
from servicios.backend.src.core.seeds import seedsUsuario
from servicios.backend.src.core.seeds import seedsStans
from models import db
from servicios.backend.src.web.controllers.mails import bp as mails_bp
from servicios.backend.src.web.controllers.muestras import bp as muestras_bp
from servicios.backend.src.web.controllers.informes import bp as informes_bp
from servicios.backend.src.web.controllers.usuarios import bp as usuarios_bp
from servicios.backend.src.web.controllers.auth import bp as auth_bp
from servicios.backend.src.web.controllers.stans import bp as stans_bp
from servicios.backend.src.core.seeds import seedsLegajo 
from flask_cors import CORS
from flask_session import Session
from flask_bcrypt import Bcrypt

session = Session()
bcrypt = Bcrypt()


def create_app(env="development", static_folder=""):
    app = Flask(__name__)
    app.config.from_object(config[env])
    db.init_app(app)
    session.init_app(app)
    bcrypt.init_app(app)

    CORS(app)
    @app.route("/")
    def home():
        return "SLAY"

    app.register_blueprint(mails_bp)
    app.register_blueprint(muestras_bp)
    app.register_blueprint(informes_bp)
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
        seedsMuestra.seeds_muestras()
        print("Muestras creadas!")
        seedsMails.seeds_mails()
        print("Mails creados!")
        seedsStans.seed_stans()
        print("Stans y ensayos creados!")
        seedsUsuario.seeds_usuarios()
        print("Usuarios creados!")

    return app
    
