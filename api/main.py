import os

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restful import Api
from webargs.flaskparser import parser, abort

from api.models.BaseModel import db
from api.resources.LoginApi import LoginApi
from api.resources.SignupApi import SignupApi
from api.resources.AuthCheckApi import AuthCheckApi
from api.resources.MonitoringApi import MonitoringApi
from api.resources.MonitorApi import MonitorApi


def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()


def init_routes(api):
    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(AuthCheckApi, '/auth/check')
    api.add_resource(MonitoringApi, '/monitoring')
    api.add_resource(MonitorApi, '/monitoring/<monitor_id>')


@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    abort(error_status_code or 422, status='error', messages=err.messages.get('json'))


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ.get('FLASK_APP_SETTINGS'))

    api_blueprint = Blueprint('api', __name__)

    api = Api(api_blueprint)
    CORS(api_blueprint)

    init_routes(api)

    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    init_db(app)
    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run()
