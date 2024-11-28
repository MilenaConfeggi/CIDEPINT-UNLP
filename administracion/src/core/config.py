from os import urandom

class Config(object):
    TESTING = False
    SECRET_KEY = urandom(24).hex()
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root123@127.0.0.1:3306/cidepint"
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
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}