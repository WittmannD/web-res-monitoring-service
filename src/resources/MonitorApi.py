from http import HTTPStatus

from flask import make_response
from flask_restful import Resource

from src.models.MonitorModel import MonitorModel
from src.models.Schemas.MonitorSchema import monitor_summary, MonitorSchema
from src.models.UserModel import UserModel
from src.utils.utils import token_required, ResponseData, ApiError, verified_email_required


class MonitorApi(Resource):
    @staticmethod
    @token_required
    @verified_email_required
    def get(current_user: UserModel, monitor_id):
        monitor = MonitorModel.find_by_first(id=monitor_id, user_id=current_user.id)

        if monitor is None:
            raise ApiError('Not found', status=HTTPStatus.NOT_FOUND)

        return ResponseData(monitor_summary.dump(monitor))

    @staticmethod
    @token_required
    @verified_email_required
    def delete(current_user: UserModel, monitor_id):
        monitor = MonitorModel.find_by_first(id=monitor_id, user_id=current_user.id)

        if monitor is None:
            raise ApiError('Not found', status=HTTPStatus.NOT_FOUND)

        monitor.delete_from_db()
        return make_response({}, HTTPStatus.NO_CONTENT)

    @staticmethod
    @token_required
    @verified_email_required
    @MonitorSchema.validate_fields(location='json')
    def patch(current_user: UserModel, args, monitor_id):
        monitor = MonitorModel.find_by_first(id=monitor_id, user_id=current_user.id)

        if monitor is None:
            raise ApiError('Not found', status=HTTPStatus.NOT_FOUND)

        for key, value in args.items():
            setattr(monitor, key, value)

        monitor.save_to_db()
        return ResponseData(monitor_summary.dump(monitor))
