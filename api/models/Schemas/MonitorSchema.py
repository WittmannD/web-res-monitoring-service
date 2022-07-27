from marshmallow import fields
from marshmallow_enum import EnumField

from .BaseSchema import BaseSchema
from ...utils.constants import HttpMethod, MonitorStatus


class MonitorSchema(BaseSchema):
    url = fields.URL(required=True)
    method = EnumField(HttpMethod, default=HttpMethod.GET)
    interval = fields.Integer(default=5)

    status = EnumField(MonitorStatus, dump_only=True, default=MonitorStatus.UP)
    next_check_at = fields.DateTime(dump_only=True)
    user_id = fields.Integer(dump_only=True)


monitor_summary = MonitorSchema(exclude=['user_id'])
