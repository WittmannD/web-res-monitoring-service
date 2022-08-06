from flask_restful import Resource
from sqlalchemy import and_

from api.models.UserModel import UserModel
from api.models.MonitorRequestsModel import MonitorRequestsModel
from api.models.Schemas.MonitorRequestsSchema import MonitorRequestsSchema, monitor_requests_summary
from api.utils.utils import token_required, ResponseData


class MonitorRequestsApi(Resource):
    @staticmethod
    @token_required
    @MonitorRequestsSchema.validate_fields(location='query')
    def get(current_user: UserModel, args, monitor_id):
        start = args.get('datetime_start')
        end = args.get('datetime_end')

        period_stmt = True
        if start is not None and end is not None:
            period_stmt = and_(
                MonitorRequestsModel.timestamp >= start,
                MonitorRequestsModel.timestamp <= end
            )
        elif start is not None:
            period_stmt = MonitorRequestsModel.timestamp >= start
        elif end is not None:
            period_stmt = MonitorRequestsModel.timestamp <= end

        monitor_requests_pagination = MonitorRequestsModel.find_paginate_and_order_by(
            page=args.get('page'),
            per_page=args.get('per_page'),
            order_by=args.get('sort'),
            monitor_id=monitor_id,
            stmt=period_stmt
        )
        print(period_stmt)
        print(monitor_requests_pagination.items)

        return ResponseData(monitor_requests_summary.dump(monitor_requests_pagination))
