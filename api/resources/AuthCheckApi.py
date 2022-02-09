from flask import request
from flask_restful import Resource
from jwt import DecodeError

from api.utils.utils import ResponseData, check_token_expiration


class AuthCheckApi(Resource):
    @staticmethod
    def get():
        token = None

        try:
            if 'Authorization' in request.headers:
                _, token = request.headers['Authorization'].split(' ')

            if token and check_token_expiration(token):
                return ResponseData([{'token': token, 'auth': True}])

        except (ValueError, DecodeError):
            pass

        finally:
            return ResponseData([{'token': '', 'auth': False}])
