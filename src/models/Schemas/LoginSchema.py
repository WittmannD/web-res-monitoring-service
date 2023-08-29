from marshmallow import fields

from src.models.Schemas.BaseSchema import ValidatedSchema


class LoginSchema(ValidatedSchema):
    email = fields.Email(
        required=True,
    )

    password = fields.Str(
        load_only=True,
        required=True
    )
