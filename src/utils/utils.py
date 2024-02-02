import datetime
import math
import traceback
from dataclasses import dataclass
from functools import wraps
from http import HTTPStatus
from typing import List, Any, Optional, Dict, Union

import jwt
from flask_restful import abort
from flask import make_response, jsonify, request, current_app, Response
from marshmallow import ValidationError
from sqlalchemy import select, func, delete
from werkzeug.exceptions import UnprocessableEntity, HTTPException

from src.models.UserModel import UserModel


@dataclass
class Response:
    content: Any
    status: str


class ApiError(Exception):
    def __init__(self, message: str, messages: Optional[Dict[str, str]] = None,
                 status: Union[HTTPStatus, int] = HTTPStatus.INTERNAL_SERVER_ERROR):
        self.status = status
        self.message = message

        if messages is not None:
            self.messages = messages

    def to_dict(self):
        return self.__dict__


def ResponseData(data: Any, status=HTTPStatus.OK):
    return make_response(
        jsonify(Response(
            content=data,
            status='success',
        )), status
    )


def ResponseDataCollection(data: List[Any], total: Optional[int] = None, status=HTTPStatus.OK):
    total = total or len(data)
    return make_response(
        jsonify(Response(
            content=dict(
                items=data,
                total=total
            ),
            status='success',
        )), status
    )


def handle_error(error):
    if isinstance(error, UnprocessableEntity):
        return abort(
            error.code,
            status='error',
            messages=error.data.get('messages'),
            traceback=traceback.format_exc() if current_app.config.get('ENV') == 'development' else None
        )

    if isinstance(error, ApiError):
        return abort(
            error.status.value if isinstance(error.status, HTTPStatus) else error.status,
            status='error',
            message=error.message,
            traceback=traceback.format_exc() if current_app.config.get('ENV') == 'development' else None
        )

    return abort(HTTPStatus.INTERNAL_SERVER_ERROR)


def decode_access_token(token):
    return jwt.decode(token, current_app.config.get('SECRET_KEY'), 'HS256')


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        try:
            if 'Authorization' not in request.headers:
                raise AssertionError()

            _, token = request.headers['Authorization'].split(' ')

            if token:
                data = decode_access_token(token)
                current_user = UserModel.find_by_id(data.get('id'))

                if current_user is None or data.get('token_type') != 'ACCESS_TOKEN':
                    raise AssertionError()

                return f(*args, current_user, **kwargs)

        except (ValueError, AssertionError, jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError) as err:
            raise ApiError('Valid access token is missing', status=HTTPStatus.UNAUTHORIZED)

    return decorator


def verified_email_required(f):
    @wraps(f)
    def decorator(current_user: UserModel, *args, **kwargs):
        if not current_user.email_verified:
            raise ApiError('Your account has not been activated. Verify your email address first',
                           status=HTTPStatus.FORBIDDEN)

        return f(*args, current_user, **kwargs)

    return decorator


def ceil_round_to_base(n, base: int):
    return base * math.ceil(n / base)


def round_to_base(n, base: int):
    return base * round(n / base)


def round_time_to_minutes(dt: datetime, base_minutes: int) -> datetime:
    return dt.replace(minute=0, second=0) + datetime.timedelta(minutes=round_to_base(dt.minute, base_minutes))


def remove_overlimit(limit: int, mapper, connection, target, filter_by: str):
    count = (
        connection
        .scalar(
            select(func.count())
            .select_from(mapper)
            .where(mapper.c[filter_by] == target.__dict__.get(filter_by))
        )
    )

    if count > limit:
        connection.execute(
            delete(mapper)
            .where(
                mapper.c.id.in_(
                    select(mapper.c.id)
                    .where(mapper.c[filter_by] == target.__dict__.get(filter_by))
                    .order_by(mapper.c.created_at.asc()).limit(count - limit + 1)
                )
            )
        )
