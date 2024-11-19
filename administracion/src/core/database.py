from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    """
    Inicializa la base de datos con la aplicación de Flask
    """

    db.init_app(app)
    config(app)
    return app


def config(app):
    """
    Configuración de Hooks para la Base de Datos
    """

    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()

    return app


def reset():
    """
    Resetea la base de datos
    """
    db.drop_all()
    db.create_all()
