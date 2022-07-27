from flask_restful import Resource

from api.models.UserModel import UserModel
from api.models.MonitorRequestsModel import MonitorRequestsModel
from api.models.Schemas.MonitorRequestsSchema import MonitorRequestsSchema, monitor_requests_summary
from api.utils.utils import token_required, ResponseData


class MonitorRequestsApi(Resource):
    @staticmethod
    @token_required
    @MonitorRequestsSchema.validate_fields(location='query')
    def get(current_user: UserModel, args, monitor_id):
        monitor_requests_pagination = MonitorRequestsModel.find_and_paginated_order_by(
            page=args.get('page'),
            per_page=args.get('per_page'),
            order_by=args.get('order_by'),
            monitor_id=monitor_id
        )

        return ResponseData(monitor_requests_summary.dump(monitor_requests_pagination))
