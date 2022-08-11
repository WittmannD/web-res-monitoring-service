import os


class Config(object):
    PORT = os.environ.get('PORT')
    PUBLIC_URL = os.environ.get('PUBLIC_URL')

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

    SMTP_HOST = os.environ.get('SMTP_HOST')
    SMTP_PORT = os.environ.get('SMTP_PORT')
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    SMTP_FROM = os.environ.get('SMTP_FROM')


class ProductionConfig(Config):
    ENV = 'production'
    FLASK_ENV = 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    ENV = 'development'
    FLASK_ENV = 'development'
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_ECHO = False
    SECRET_KEY = 'development_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
