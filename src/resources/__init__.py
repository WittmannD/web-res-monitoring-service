from flask import Blueprint
from flask_restful import Api

from src.resources.LoginApi import LoginApi
from src.resources.SignupApi import SignupApi
from src.resources.SendVerificationApi import SendVerificationApi
from src.resources.EmailVerificationApi import EmailVerificationApi
from src.resources.UserApi import UserApi
from src.resources.MonitoringApi import MonitoringApi
from src.resources.MonitorApi import MonitorApi
from src.resources.MonitorRequestsApi import MonitorRequestsApi
from src.resources.EventsApi import EventsApi
from src.resources.static.index import blueprint as index_blueprint
from src.utils import constants
from src.utils.utils import handle_error

blueprint = Blueprint('api', __name__)
api = Api(blueprint)


def register_resources(app):
    api.add_resource(LoginApi, constants.LOGIN_ROUTE)
    api.add_resource(SignupApi, constants.SIGNUP_ROUTE)
    api.add_resource(SendVerificationApi, constants.SEND_EMAIL_ROUTE)
    api.add_resource(EmailVerificationApi, constants.VERIFICATION_ROUTE)

    api.add_resource(UserApi, constants.USER_ROUTE)

    api.add_resource(MonitoringApi, constants.MONITORING_ROUTE)
    api.add_resource(MonitorRequestsApi, constants.MONITOR_REQUESTS_ROUTE)
    api.add_resource(MonitorApi, constants.SINGLE_MONITOR_ROUTE)
    api.add_resource(EventsApi, constants.EVENTS_ROUTE)

    blueprint.register_error_handler(Exception, handle_error)
    app.register_blueprint(blueprint, url_prefix=constants.API_PREFIX)
    app.register_blueprint(index_blueprint)
