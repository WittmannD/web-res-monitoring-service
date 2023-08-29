import os
import pathlib

from flask import Flask

from src.resources import register_resources
from src.extensions import register_extensions
from src.configuration import config


def create_app():
    app = Flask(__name__, static_folder=pathlib.Path(__file__).parent.resolve().joinpath('client', 'build'))

    app.config.from_object(config)

    register_extensions(app)
    register_resources(app)

    return app


def create_worker_app():
    """Minimal App without routes for celery worker."""
    app = Flask(__name__)

    app.config.from_object(config)

    register_extensions(app)

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(port=os.environ.get('PORT'), threaded=True)
