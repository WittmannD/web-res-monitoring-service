from marshmallow import fields
from marshmallow_enum import EnumField

from .BaseSchema import BaseSchema
from ...utils.constants import HttpMethod


class MonitorSchema(BaseSchema):
    url = fields.URL(required=True)
    method = EnumField(HttpMethod, default=HttpMethod.GET)
    interval = fields.Integer(default=5)

    next_check_at = fields.DateTime(dump_only=True)
    user_id = fields.Integer(dump_only=True)


monitor_summary = MonitorSchema(exclude=['user_id'])
