
from flask_wtf.csrf import CSRFError
from flask import render_template

def registrar_handlers(app):

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('csrf_error.html', error_message=e.description), 400
    return app