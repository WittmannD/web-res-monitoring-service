from hmac import compare_digest

from marshmallow import fields, validate, validates_schema, ValidationError

from api.models.Schemas.BaseSchema import ValidatedSchema


class SignupSchema(ValidatedSchema):
    email = fields.Email(
        required=True,
        error_messages={'required': 'This field is required'}
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
