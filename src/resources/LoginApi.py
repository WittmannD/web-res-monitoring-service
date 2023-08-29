from http import HTTPStatus

from flask_restful import Resource

from src.models.Schemas.LoginSchema import LoginSchema
from src.models.Schemas.TokensSchema import access_token_summary
from src.models.UserModel import UserModel
from src.utils.utils import ResponseData, ApiError


class LoginApi(Resource):
    @staticmethod
    @LoginSchema.validate_fields(location="json")
    def post(args):
        user = UserModel.find_by_email(args.get('email'))

        if user is None or not UserModel.verify_hash(user.password, args.get('password')):
            raise ApiError('Invalid email or password', status=HTTPStatus.UNAUTHORIZED)

        return ResponseData(dict(access_token=access_token_summary.dump(user)))
