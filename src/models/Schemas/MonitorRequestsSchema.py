from marshmallow import post_dump, fields, post_load
from marshmallow_enum import EnumField

from src.models.Schemas.BaseSchema import BaseSchema
from src.models.Schemas.PaginationSchema import PaginationSchema
from src.utils.constants import MonitorStatus


class MonitorRequestSchema(BaseSchema):
    timestamp = fields.DateTime(nullable=False)
    elapsed = fields.Float(nullable=False)
    status_code = EnumField(MonitorStatus, default=MonitorStatus.UP, nullable=False)
    response = fields.String(nullable=False)
    monitor_id = fields.Integer(dump_only=True)


monitor_request_summary = MonitorRequestSchema(exclude=['monitor_id'])


class MonitorRequestsSchema(PaginationSchema):
    datetime_start = fields.DateTime(load_only=True)
    datetime_end = fields.DateTime(load_only=True)

    @post_load()
    def process_input_data(self, data, **kwargs):
        self.validate_sort_parameters(data, monitor_request_summary)
        return data

    @post_dump()
    def process_dump(self, data, **kwargs):
        data['items'] = monitor_request_summary.dump(data.get('items', []), many=True)
        return data


monitor_requests_summary = MonitorRequestsSchema()
