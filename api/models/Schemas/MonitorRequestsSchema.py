from typing import Union
from datetime import datetime

from marshmallow import post_dump, fields
from marshmallow_enum import EnumField

from api.models.Schemas.BaseSchema import BaseSchema
from api.models.Schemas.PaginationSchema import PaginationSchema
from api.utils.constants import MonitorStatus


class MonitorRequestSchema(BaseSchema):
    timestamp: datetime
    elapsed: Union[int, float]
    status_code: MonitorStatus
    response: str
    monitor_id: int

    timestamp = fields.DateTime(nullable=False)
    elapsed = fields.Number(nullable=False)
    status_code = EnumField(MonitorStatus, default=MonitorStatus.UP, nullable=False)
    response = fields.String(nullable=False)
    monitor_id = fields.Integer(dump_only=True)


monitor_request_summary = MonitorRequestSchema(exclude=['monitor_id'])


class MonitorRequestsSchema(PaginationSchema):
    @post_dump()
    def process_dump(self, data, **kwargs):
        data['items'] = monitor_request_summary.dump(data.get('items', []), many=True)
        return data


monitor_requests_summary = MonitorRequestsSchema()
