from os import getenv, urandom
from flask import Flask
from flask_wtf import CSRFProtect
from flask_session import Session
from flask_login import LoginManager
from administracion.src.core.database import db
from administracion.src.core.config import config
from administracion.src.web.controllers.rutas import registrar_rutas
from administracion.src.web.handlers.handlers import registrar_handlers
from administracion.src.core.bcrypt import bcrypt
from administracion.src.web.controllers.personal.area_controller import area_bp
from administracion.src.web.controllers.personal.personal_controller import personal_bp
from administracion.src.web.controllers.personal.ausencia_controller import ausencia_bp
from administracion.src.web.controllers.auth_controller import auth_bp
from models.personal.area import Area 
from sqlalchemy.sql import text
from models.personal.personal import User
from datetime import datetime
from administracion.src.core import database
def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    app.config["SECRET_KEY"] = getenv("SECRET_KEY", urandom(24).hex())
    
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
    app = registrar_rutas(app)
    app = registrar_handlers(app)

    # Register blueprints
    app.register_blueprint(area_bp)
    app.register_blueprint(personal_bp)
    app.register_blueprint(ausencia_bp)
    app.register_blueprint(auth_bp)


    @app.cli.command(name="reset-db")
    def reset_db():
     """Reset the database (drop and recreate tables)."""
    with app.app_context():
        try:
            # Conexión directa al motor
            with db.engine.connect() as connection:
                # Desactivar restricciones de claves foráneas
                connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
                
                # Eliminar todas las tablas
                db.drop_all()
                
                # Reactivar restricciones de claves foráneas
                connection.execute("SET FOREIGN_KEY_CHECKS = 1;")
                
                # Crear todas las tablas nuevamente
                db.create_all()
            
            print("Database has been reset successfully.")
        except Exception as e:
            print(f"Error resetting database: {e}")
    @app.cli.command(name="seeds-db")
    def seed_db():
        database.seed()
        
    
    @app.cli.command(name="create-admin")
    def create_admin():
        with app.app_context():
            # Asegúrate de que el área por defecto existe
            default_area = Area.query.get(1)
            if not default_area:
                default_area = Area(nombre='Default Area', saldo=0)
                db.session.add(default_area)
                db.session.commit()
                print("Área por defecto creada con éxito.")
            else:
                print("Área por defecto ya existe.")
            
            # Crear usuario administrador si no existe
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(
                    username='admin',
                    password='admin',
                    email='admin@example.com',
                    area_id=default_area.id,  # Asigna el área creada
                    dni='00000000',
                    nombre='Admin',
                    apellido='User',
                    dependencia='UNLP',
                    cargo='Administrativo',
                    subdivision_cargo='Ley 10430',
                    telefono='123456789',
                    domicilio='Admin Address',
                    fecha_nacimiento=datetime.strptime('1970-01-01', '%Y-%m-%d'),
                    observaciones='Usuario administrador por defecto',
                    habilitado=True,
                    rol='Administrador'
                )
                db.session.add(admin_user)
                db.session.commit()
                print("Usuario administrador creado con éxito.")
            else:
                print("Usuario administrador ya existe.")


    return app