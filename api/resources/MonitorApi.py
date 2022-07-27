from http import HTTPStatus

from flask import make_response
from flask_restful import Resource

from api.models.MonitorModel import MonitorModel
from api.models.Schemas.MonitorSchema import monitor_summary
from api.models.UserModel import UserModel
from api.utils.utils import token_required, ResponseData, ResponseError


class MonitorApi(Resource):
    @token_required
    def get(self, current_user: UserModel, monitor_id):
        monitor = MonitorModel.find_by_first(id=monitor_id, user_id=current_user.id)

        if monitor:
            return ResponseData(monitor_summary.dump(monitor))

        else:
            return ResponseError('Not found', HTTPStatus.NOT_FOUND)

    @token_required
    def delete(self, current_user: UserModel, monitor_id):
        monitor = MonitorModel.find_by_first(id=monitor_id, user_id=current_user.id)

        if monitor:
            monitor.delete_from_db()
            return make_response(HTTPStatus.NO_CONTENT)

        else:
            return ResponseError('Not found', HTTPStatus.NOT_FOUND)
