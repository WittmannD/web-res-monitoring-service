from flask import make_response
from flask_restful import Resource

from api.models.MonitorModel import MonitorModel
from api.models.UserModel import UserModel
from api.utils.utils import token_required, ResponseData, ResponseError


class MonitorApi(Resource):
    @token_required
    def get(self, current_user: UserModel, monitor_id):
        monitor = MonitorModel.find_by_id(monitor_id)

        if monitor:
            return ResponseData(monitor)

        else:
            return ResponseError('Not found', 404)

    @token_required
    def delete(self, current_user: UserModel, monitor_id):
        monitor = MonitorModel.find_by_id(monitor_id)

        if monitor:
            monitor.delete_from_db()
            return make_response(400)

        else:
            return ResponseError('Not found', 404)
