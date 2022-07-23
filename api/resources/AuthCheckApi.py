from flask import request
from flask_restful import Resource
from jwt import DecodeError, ExpiredSignatureError

from api.utils.utils import ResponseData, decode_access_token


class AuthCheckApi(Resource):
    @staticmethod
    def get():
        token = None

        try:
            if 'Authorization' in request.headers:
                _, token = request.headers['Authorization'].split(' ')

            if token:
                decode_access_token(token)
                return ResponseData({'access_token': token, 'auth': True})

        except (ValueError, DecodeError, ExpiredSignatureError):
            return ResponseData({'access_token': '', 'auth': False})
