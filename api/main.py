import os

from dotenv import load_dotenv
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS
from flask_restful import Api

from api.models.BaseModel import db
from api.resources.EmailVerificationApi import EmailVerificationApi
from api.resources.SendVerificationApi import SendVerificationApi
from api.resources.EventsApi import EventsApi
from api.resources.LoginApi import LoginApi
from api.resources.MonitorRequestsApi import MonitorRequestsApi
from api.resources.SignupApi import SignupApi
from api.resources.UserApi import UserApi
from api.resources.MonitoringApi import MonitoringApi
from api.resources.MonitorApi import MonitorApi
import api.utils.constants as constants
from api.utils.utils import handle_error


def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()


def init_routes(api):
    api.add_resource(LoginApi, constants.LOGIN_ROUTE)
    api.add_resource(SignupApi, constants.SIGNUP_ROUTE)
    api.add_resource(SendVerificationApi, constants.SEND_EMAIL_ROUTE)
    api.add_resource(EmailVerificationApi, constants.VERIFICATION_ROUTE)

    api.add_resource(UserApi, constants.USER_ROUTE)

    api.add_resource(MonitoringApi, constants.MONITORING_ROUTE)
    api.add_resource(MonitorRequestsApi, constants.MONITOR_REQUESTS_ROUTE)
    api.add_resource(MonitorApi, constants.SINGLE_MONITOR_ROUTE)
    api.add_resource(EventsApi, constants.EVENTS_ROUTE)


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.register_error_handler(Exception, handle_error)

    app.config.from_object(os.environ.get('FLASK_APP_SETTINGS'))
    init_db(app)

    api_blueprint = Blueprint('api', __name__)

    api = Api(api_blueprint)
    CORS(api_blueprint)

    init_routes(api)

    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(port=flask_app.config.get('PORT'))
