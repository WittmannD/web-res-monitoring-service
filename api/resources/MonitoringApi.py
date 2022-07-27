from http import HTTPStatus

from flask_restful import Resource

from api.models.MonitorModel import MonitorModel
from api.models.Schemas.MonitorSchema import MonitorSchema, monitor_summary
from api.models.Schemas.MonitoringSchema import MonitoringSchema, monitoring_summary
from api.models.UserModel import UserModel
from api.utils.utils import token_required, ResponseData


class MonitoringApi(Resource):
    @staticmethod
    @token_required
    @MonitoringSchema.validate_fields(location='query')
    def get(current_user: UserModel, args):
        monitors_pagination = MonitorModel.find_and_paginated_order_by(
            page=args.get('page'),
            per_page=args.get('per_page'),
            order_by=args.get('order_by'),
            user_id=current_user.id
        )

        return ResponseData(monitoring_summary.dump(monitors_pagination))

    @staticmethod
    @token_required
    @MonitorSchema.validate_fields(location='json')
    def post(current_user: UserModel, args):
        monitor = MonitorModel(
            url=args.get('url'),
            method=args.get('method'),
            interval=args.get('interval'),
            user_id=current_user.id,
            next_check_at=None,
            status=None
        )

        monitor.save_to_db()

        return ResponseData(monitor_summary.dump(monitor), status=HTTPStatus.CREATED)
