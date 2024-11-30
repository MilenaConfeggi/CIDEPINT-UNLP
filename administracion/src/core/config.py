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
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root123@127.0.0.1:3306/cidepint"
    SECRET_KEY = urandom(24).hex()
    SESSION_TYPE = "filesystem"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}