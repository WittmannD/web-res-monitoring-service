import os

BASEDIR = os.path.abspath(os.path.dirname(__name__))


class Config(object):
    ENV = os.environ.get('FLASK_ENV', 'development')
    PORT = os.environ.get('PORT')
    PUBLIC_URL = os.environ.get('PUBLIC_URL')

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DATABASE = os.environ.get('POSTGRES_DATABASE')

    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DATABASE}'
    DATABASE_URL = SQLALCHEMY_DATABASE_URI

    SMTP_HOST = os.environ.get('SMTP_HOST')
    SMTP_PORT = os.environ.get('SMTP_PORT')
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    SMTP_FROM = os.environ.get('SMTP_FROM')

    SECRET_KEY = os.environ.get('SECRET_KEY')

    BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL = BROKER_URL
    CELERY_TIMEZONE = os.environ.get("CELERY_TIMEZONE", "Europe/Berlin")
    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
    )
    CELERY_SEND_SENT_EVENT = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_ECHO = False
    SECRET_KEY = 'development_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


available_configs = dict(development=DevelopmentConfig, production=ProductionConfig)
selected_config = os.getenv("FLASK_ENV", "production")
config = available_configs.get(selected_config, "production")
