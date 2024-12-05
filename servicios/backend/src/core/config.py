from os import getenv, urandom
from dotenv import load_dotenv

load_dotenv()

class Config():
    TESTING = False
    SECRET_KEY = getenv('SECRET_KEY', urandom(24).hex())
    SESSION_TYPE = "filesystem"
class DevelopmentConfig(Config):
    PORT = getenv("PORT")
    DB_NAME = getenv("DB_NAME")
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    print(PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)
    JWT_SECRET_KEY = 'soy secreta 0.o'  # Cambia esto por una clave segura
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hora


config = {
    "development": DevelopmentConfig,
    #"production": ProductionConfig,
    #"testing": TestingConfig,
}