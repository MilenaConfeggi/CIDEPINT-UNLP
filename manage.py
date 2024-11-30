#!/usr/bin/env python
import os
import sys
from flask.cli import FlaskGroup
from servicios.backend.src.web import create_app as create_servicios_app

def main():
    if len(sys.argv) < 2:
        print("Usage: manage.py <app_name> [flask_args]")
        sys.exit(1)

    app_name = sys.argv[1]
    print(app_name)
    flask_args = sys.argv[2:]

    if app_name == "servicios":
        os.environ.setdefault("FLASK_APP", "servicios.backend.src.web:create_app()")
        create_app = create_servicios_app
    elif app_name == "administracion":
        from administracion.src.web import create_app as create_administracion_app
        os.environ.setdefault("FLASK_APP", "administracion.src.web:create_app()")
        create_app = create_administracion_app
    else:
        print(f"Unknown app name: {app_name}")
        sys.exit(1)

    os.environ.setdefault("FLASK_ENV", "development")
    try:
        app = create_app()
        cli = FlaskGroup(create_app=create_app)
        cli.main(args=flask_args)
    except Exception as exc:
        raise RuntimeError(
            "Couldn't start Flask application. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

if __name__ == "__main__":
    main()