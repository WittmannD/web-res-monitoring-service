import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    ENV = "development"
    FLASK_ENV = "development"
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_ECHO = True
    SECRET_KEY = 'development_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
