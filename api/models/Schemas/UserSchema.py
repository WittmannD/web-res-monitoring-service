from marshmallow import fields, validate, pre_load, post_dump

from .BaseSchema import BaseSchema
from ...utils.utils import create_access_token


class UserSchema(BaseSchema):
    username = fields.String(
        required=True,
        location='json',
        error_messages={'required': 'This field is required'},
        validate=[validate.Length(min=4, max=24), validate.Regexp(regex=r'^[a-zA-Z0-9_.-]+$')],
    )

    password = fields.Str(
        load_only=True,
        required=True,
        validate=[validate.Length(min=6)]
    )

    password_confirmation = fields.Str(required=False, load_only=True)

    @pre_load()
    def user_details_strip(self, data, **kwargs):
        data['username'] = data.get('username').lower().strip()
        return data

    @post_dump()
    def create_access_token(self, data, **kwargs):
        return create_access_token(data)


user_summary = UserSchema()
