from flask import Flask
import os
import sys
import importlib
from servicios.backend.src.core.config import config
from models import db, MedioDePago

def create_app(env="development", static_folder=""):
    app = Flask(__name__)
    app.config.from_object(config[env])
    db.init_app(app)
    @app.route("/")
    def home():
        return "SLAY"
    
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

    return app
    
