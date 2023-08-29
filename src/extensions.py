import os

from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
celery = Celery()


def register_extensions(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()

    celery.config_from_object(app.config)
    CORS(app)
