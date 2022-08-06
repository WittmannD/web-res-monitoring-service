import datetime
import math
import traceback
from dataclasses import dataclass
from functools import wraps
from http import HTTPStatus
from typing import List, Any, Optional

import jwt
from flask import make_response, jsonify, request, current_app, Response
from flask_sqlalchemy import Model
from sqlalchemy import select, func, delete

from api.models.UserModel import UserModel


@dataclass
class Response:
    content: Any
    status: str


@dataclass
class Error:
    message: str
    status: str


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


def ResponseError(message: str, err_code: int):
    return make_response(
        jsonify(Error(
            message=message,
            status='error'
        )), err_code
    )


def create_access_token(user_data):
    return jwt.encode(
        {
            'id': user_data['id'],
            'username': user_data['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=360)
        },
        key=current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )


def decode_access_token(token):
    return jwt.decode(token, current_app.config.get('SECRET_KEY'), 'HS256')


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        try:
            if 'Authorization' in request.headers:
                _, token = request.headers['Authorization'].split(' ')

            if token:
                data = decode_access_token(token)
                current_user = UserModel.find_by_id(data.get('id'))
                if current_user is None:
                    raise ValueError()

                return f(*args, current_user, **kwargs)

        except (ValueError, jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError) as err:
            return ResponseError('Valid access token is missing', HTTPStatus.UNAUTHORIZED)

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
