from http import HTTPStatus

from flask_restful import Resource
from sqlalchemy import and_

from src.models.MonitorModel import MonitorModel
from src.models.Schemas.MonitorSchema import MonitorSchema, monitor_summary
from src.models.Schemas.MonitoringSchema import MonitoringSchema, monitoring_summary
from src.models.UserModel import UserModel
from src.utils.utils import token_required, ResponseData, ApiError, verified_email_required


class MonitoringApi(Resource):
    @staticmethod
    @token_required
    @verified_email_required
    @MonitoringSchema.validate_fields(location='query')
    def get(current_user: UserModel, args):
        monitors_pagination = MonitorModel.find_paginate_and_order_by(
            page=args.get('page'),
            per_page=args.get('per_page'),
            order_by=args.get('sort'),
            user_id=current_user.id
        )

        return ResponseData(monitoring_summary.dump(monitors_pagination))

    @staticmethod
    @token_required
    @verified_email_required
    @MonitorSchema.validate_fields(location='json')
    def post(current_user: UserModel, args):
        running_monitors = MonitorModel.count_by(and_(
            MonitorModel.running,
            MonitorModel.user_id == current_user.id
        ))

        if running_monitors >= 3:
            raise ApiError('Active monitor limit exceeded', status=HTTPStatus.FORBIDDEN)

        monitor = MonitorModel(
            url=args.get('url'),
            method=args.get('method'),
            running=args.get('running'),
            interval=args.get('interval'),
            user_id=current_user.id,
            next_check_at=None,
            status=None
        )

        monitor.save_to_db()

        return ResponseData(monitor_summary.dump(monitor), status=HTTPStatus.CREATED)
