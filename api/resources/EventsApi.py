from flask_restful import Resource

from api.models import EventsModel
from api.models.Schemas.EventsSchema import events_summary, EventsSchema
from api.models.UserModel import UserModel
from api.utils.utils import token_required, ResponseData, verified_email_required


class EventsApi(Resource):
    @staticmethod
    @token_required
    @verified_email_required
    @EventsSchema.validate_fields(location='query')
    def get(current_user: UserModel, args):
        events_pagination = EventsModel.find_paginate_and_order_by(
            page=args.get('page'),
            per_page=args.get('per_page'),
            order_by=args.get('order_by'),
            user_id=current_user.id
        )

        return ResponseData(events_summary.dump(events_pagination))
