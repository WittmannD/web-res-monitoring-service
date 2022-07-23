from marshmallow import fields, validate, post_dump

from .BaseSchema import BaseSchema
from ...utils.utils import create_access_token


class UserSchema(BaseSchema):
    username = fields.String(
        required=True,
        error_messages={'required': 'This field is required'},
        validate=[validate.Length(min=4, max=24), validate.Regexp(regex=r'^[a-zA-Z0-9_.-]+$')],
    )

    @post_dump()
    def create_access_token(self, data, **kwargs):
        return create_access_token(data)


user_summary = UserSchema()
