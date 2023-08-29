from http import HTTPStatus

from flask_restful import Resource

from src.models.Schemas.TokensSchema import access_token_summary
from src.models.Schemas.SignupSchema import SignupSchema
from src.models.UserModel import UserModel
from src.utils.utils import ResponseData, ApiError


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
