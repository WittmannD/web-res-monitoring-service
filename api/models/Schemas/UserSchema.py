from marshmallow import fields, validate, pre_dump

from .BaseSchema import BaseSchema


class UserSchema(BaseSchema):
    email = fields.Email(
        required=True,
        error_messages={'required': 'This field is required'}
    )
    email_verified = fields.Boolean(default=False)


user_summary = UserSchema()
