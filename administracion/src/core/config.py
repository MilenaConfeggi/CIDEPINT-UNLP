from os import getenv, environ, urandom
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    TESTING = False
    SECRET_KEY = getenv('SECRET_KEY', urandom(24).hex())
    SESSION_TYPE = "filesystem"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }


class DevelopmentConfig(Config):
    DB_USER = getenv("DB_USER", "postgres")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST", "localhost")
    DB_PORT = getenv("PORT", "5432")
    DB_NAME = getenv("DB_NAME", "grupo18")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SECRET_KEY = getenv("SECRET_KEY", urandom(24).hex())
    SESSION_TYPE = "filesystem"


class TestingConfig(Config):
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
