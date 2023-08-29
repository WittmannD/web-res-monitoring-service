from http import HTTPStatus

from marshmallow import post_dump, fields, post_load
from marshmallow_enum import EnumField

from src.models.Schemas.BaseSchema import BaseSchema
from src.models.Schemas.PaginationSchema import PaginationSchema
from src.utils.constants import MonitorStatus


class EventSchema(BaseSchema):
    event = EnumField(MonitorStatus, nullable=False)
    reason = EnumField(HTTPStatus, nullable=False)
    datetime = fields.DateTime(nullable=False)
    user_id = fields.Integer(dump_only=True)
    monitor_id = fields.Integer(dump_only=True)


event_summary = EventSchema(exclude=['user_id'])


class EventsSchema(PaginationSchema):
    @post_load()
    def process_input_data(self, data, **kwargs):
        self.validate_sort_parameters(data, event_summary)
        return data

    @post_dump()
    def process_dump(self, data, **kwargs):
        data['items'] = event_summary.dump(data.get('items', []), many=True)
        return data


events_summary = EventsSchema()
