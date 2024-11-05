from flask import Flask
def create_app(env="development", static_folder=""):
    app = Flask(__name__)
    
    @app.route("/")
    def home():
        return "SLAY"
    
    return app