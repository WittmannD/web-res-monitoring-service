from marshmallow import fields
from marshmallow_enum import EnumField

from .BaseSchema import BaseSchema
from ...utils.constants import Method


class MonitorSchema(BaseSchema):
    url = fields.URL(required=True)
    method = EnumField(Method, default=Method.GET)
    interval = fields.Integer(default=5)

    next_check_at = fields.DateTime(dump_only=True)
    user_id = fields.Integer(dump_only=True)


monitor_summary = MonitorSchema(exclude=['user_id'])
