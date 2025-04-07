from os import getenv, urandom
from flask import Flask
from flask_wtf import CSRFProtect
from flask_session import Session
from flask_login import LoginManager
from models import db
from administracion.src.core.config import config
from administracion.src.web.controllers.rutas import registrar_rutas
from administracion.src.web.handlers.handlers import registrar_handlers
from administracion.src.core.bcrypt import bcrypt
from sqlalchemy.sql import text
from administracion.src.core import database
from models.personal.personal import User

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    
    # Initialize CSRF protection
    csrf = CSRFProtect(app)
    
    # Initialize session
    sess = Session(app)

    # Initialize bcrypt
    bcrypt.init_app(app)
    
    # Initialize database
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Cambia esto según tu ruta de login

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register routes and handlers
    registrar_rutas(app)
    registrar_handlers(app)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()
    

    @app.cli.command(name="seeds-db")
    def seed_db():
        database.seed()

    @app.cli.command(name="create-admin")
    def create_admin():
        database.create_admin()
        
    return app