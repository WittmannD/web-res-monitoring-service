from hmac import compare_digest

from marshmallow import fields, validate, validates_schema, ValidationError

from api.models.Schemas.BaseSchema import ValidatedSchema


class SignupSchema(ValidatedSchema):
    username = fields.String(
        required=True,
        error_messages={'required': 'This field is required'},
        validate=[validate.Length(min=4, max=24), validate.Regexp(regex=r'^[a-zA-Z0-9_.-]+$')],
    )

    password = fields.Str(
        load_only=True,
        required=True,
        validate=[validate.Length(min=6)]
    )

    password_confirmation = fields.Str(
        required=True,
        load_only=True
    )

    @validates_schema
    def signup_schema_validation(self, data, **kwargs):
        if not compare_digest(data.get('password'), data.get('password_confirmation')):
            raise ValidationError('Password and password confirmation do not match', 'password_confirmation')
