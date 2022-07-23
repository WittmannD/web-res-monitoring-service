from marshmallow import fields, validate, validates_schema, ValidationError

from api.models.Schemas.BaseSchema import ValidatedSchema


class LoginSchema(ValidatedSchema):
    username = fields.String(
        required=True,
    )

    password = fields.Str(
        load_only=True,
        required=True
    )
