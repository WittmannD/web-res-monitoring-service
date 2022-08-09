from http import HTTPStatus

from flask_restful import Resource
from hmac import compare_digest

from api.models.Schemas.TokensSchema import access_token_summary
from api.models.Schemas.SignupSchema import SignupSchema
from api.models.Schemas.UserSchema import UserSchema, user_summary
from api.models.UserModel import UserModel
from api.utils.utils import ResponseData, ApiError


class SignupApi(Resource):
    @staticmethod
    @SignupSchema.validate_fields(location="json")
    def post(args):
        user = UserModel.find_by_email(args.get('email'))

        if user:
            raise ApiError('User with this email already exists', status=HTTPStatus.CONFLICT)

        hashed_password = UserModel.generate_hash(args.get('password'))

        new_user = UserModel(email=args.get('email'), password=hashed_password, email_verified=False)
        new_user.save_to_db()

        return ResponseData(dict(access_token=access_token_summary.dump(new_user)))
