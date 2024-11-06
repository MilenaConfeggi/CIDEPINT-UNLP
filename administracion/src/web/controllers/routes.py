from flask import render_template

def register_routes(app):
    """
    Register all the routes and blueprints for the given Flask application.
    Args:
        app (Flask): The Flask application instance to register routes with.
    Blueprints:
        
    Routes:
        - "/": Route for the landing page, renders 'landing_page.html'.
        - "/home": Route for the home page, renders 'home.html'.
    """

    @app.route("/")
    def landing_page():
        return render_template("landing_page.html")

    @app.route("/home")
    def home():
        return render_template("home.html")

    return app