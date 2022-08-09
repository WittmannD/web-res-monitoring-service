import datetime
from http import HTTPStatus

import jwt
from flask import current_app
from marshmallow import Schema, fields, post_dump, pre_load

from api.models.Schemas.BaseSchema import ValidatedSchema
from api.utils.utils import decode_access_token, ApiError


class TokenSchema(Schema):
    __abstract__ = True
    __expiration__ = datetime.timedelta(hours=360)

    exp = fields.Integer(load_only=True, required=True)

    @pre_load
    def load_from_jwt(self, data, many=False, partial=False):
        token = data.get('token')

        if isinstance(token, str):
            try:
                return decode_access_token(token)
            except (ValueError, jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError) as err:
                raise ApiError('Valid access token is missing', status=HTTPStatus.UNAUTHORIZED)

        return token

    @post_dump
    def generate_jwt(self, data, many=False):
        exp = datetime.datetime.utcnow() + self.__expiration__
        token = jwt.encode(
            {
                **data,
                'exp': exp
            },
            key=current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )

        return token


class VerificationTokenSchema(TokenSchema, ValidatedSchema):
    __expiration__ = datetime.timedelta(minutes=10)

    id = fields.Integer(required=True)

    token_type = fields.String(dump_default='VERIFICATION_TOKEN')


verification_token_summary = VerificationTokenSchema()


class AccessTokenSchema(TokenSchema):
    __expiration__ = datetime.timedelta(hours=360)

    id = fields.Integer(required=True)
    email = fields.Email(required=True)

    token_type = fields.String(dump_default='ACCESS_TOKEN')


access_token_summary = AccessTokenSchema()
