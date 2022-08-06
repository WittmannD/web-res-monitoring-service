from http import HTTPStatus

from flask import make_response
from flask_restful import Resource
from webargs.flaskparser import use_kwargs

from api.models.MonitorModel import MonitorModel
from api.models.Schemas.MonitorSchema import monitor_summary, MonitorSchema
from api.models.UserModel import UserModel
from api.utils.utils import token_required, ResponseData, ResponseError


class MonitorApi(Resource):
    @staticmethod
    @token_required
    def get(current_user: UserModel, monitor_id):
        monitor = MonitorModel.find_by_first(id=monitor_id, user_id=current_user.id)

        if monitor:
            return ResponseData(monitor_summary.dump(monitor))

        else:
            return ResponseError('Not found', HTTPStatus.NOT_FOUND)

    @staticmethod
    @token_required
    def delete(current_user: UserModel, monitor_id):
        monitor = MonitorModel.find_by_first(id=monitor_id, user_id=current_user.id)

        if monitor:
            monitor.delete_from_db()
            return make_response({}, HTTPStatus.NO_CONTENT)

        else:
            return ResponseError('Not found', HTTPStatus.NOT_FOUND)

    @staticmethod
    @token_required
    @MonitorSchema.validate_fields(location='json')
    def patch(current_user: UserModel, args, monitor_id):
        monitor = MonitorModel.find_by_first(id=monitor_id, user_id=current_user.id)

        if monitor:
            for key, value in args.items():
                setattr(monitor, key, value)

            monitor.save_to_db()
            return ResponseData(monitor_summary.dump(monitor))

        else:
            return ResponseError('Not found', HTTPStatus.NOT_FOUND)
