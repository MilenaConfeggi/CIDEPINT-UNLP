from flask import Flask, render_template
from servicios.backend.src.core.config import config
from servicios.backend.src.core.seeds import seedsMuestra
from servicios.backend.src.core.seeds import seedsMails
from models import db
from servicios.backend.src.web.controllers.mails import bp as mails_bp
from servicios.backend.src.web.controllers.muestras import bp as muestras_bp
from servicios.backend.src.web.controllers.informes import bp as informes_bp
from servicios.backend.src.core.seeds import seedsLegajo 
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
        #seedsMuestra.seeds_muestras()
        #print("Muestras creadas!")
        #seedsMails.seeds_mails()
        #print("Mails creados!")
        #seedsInforme.seeds_informe()
        #print("Documentos creados!")
        #seedsCliente.seeds_clientes()
        #print("Clientes creados!")
        seedsLegajo.seeds_legajos()
        print("Legajos creados!")

    return app
    
