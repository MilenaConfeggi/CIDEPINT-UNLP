from os import getenv, urandom
from flask import Flask, render_template, session
from flask_wtf import CSRFProtect
from flask_session import Session
from administracion.src.core import database
from administracion.src.core.config import config
from administracion.src.web.controllers.routes import register_routes
from administracion.src.web.handlers.handlers import register_handlers
from administracion.src.core.bcrypt import bcrypt


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    app.config["SECRET_KEY"] = getenv("SECRET_KEY", urandom(24).hex())
    csrf = CSRFProtect(app)
    sess = Session(app)

    bcrypt.init_app(app)
    database.init_app(app)

    app = register_routes(app)
    app = register_handlers(app)
    
    bcrypt.init_app(app)
    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()
    
    return app