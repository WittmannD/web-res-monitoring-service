from marshmallow import fields, post_load
from marshmallow_enum import EnumField

from src.models.Schemas.BaseSchema import BaseSchema
from src.utils.constants import HttpMethod, MonitorStatus


class MonitorSchema(BaseSchema):
    url = fields.URL(required=True)
    method = EnumField(HttpMethod, default=HttpMethod.GET)
    interval = fields.Integer(default=5)
    running = fields.Boolean(missing=True)

    status = EnumField(MonitorStatus, dump_only=True, default=MonitorStatus.UP)
    next_check_at = fields.DateTime(dump_only=True)
    user_id = fields.Integer(dump_only=True)


monitor_summary = MonitorSchema(exclude=['user_id'])
