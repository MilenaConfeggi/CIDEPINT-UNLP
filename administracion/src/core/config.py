from os import urandom, getenv

class Config(object):
    TESTING = False
    SECRET_KEY = urandom(24).hex()
    SESSION_TYPE = "filesystem"

class DevelopmentConfig(Config):
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("PORT")
    DB_NAME = getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)

config = {
    "development": DevelopmentConfig,
    #"production": ProductionConfig,
    #"testing": TestingConfig,
}