from os import getenv, environ, urandom

class Config(object):
    TESTING = False
    SECRET_KEY = getenv('SECRET_KEY', urandom(24).hex())
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'cidepint996@gmail.com'
    MAIL_PASSWORD = 'ovsd lfba ejyo qdha'
    MAIL_DEFAULT_SENDER = 'cidepint996@gmail.com'

class DevelopmentConfig(Config):
    DB_USER = getenv("DB_USER", "postgres")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST", "localhost")
    DB_PORT = getenv("PORT", "5432")
    DB_NAME = getenv("DB_NAME", "grupo18")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class TestingConfig(Config):
    TESTING = True


config = {
    "development": DevelopmentConfig,
    #"production": ProductionConfig,
    "testing": TestingConfig,
}