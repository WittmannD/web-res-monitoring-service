from flask_restful import Resource
from werkzeug.security import safe_str_cmp

from api.models.Schemas.UserSchema import UserSchema, user_summary
from api.models.UserModel import UserModel
from api.utils.utils import ResponseError, ResponseData


class SignupApi(Resource):
    @staticmethod
    @UserSchema.validate_fields(location="json")
    def post(args):
        if (
                not args.get('password_confirmation') or
                not safe_str_cmp(args.get('password'), args.get('password_confirmation'))
        ):
            return ResponseError('Password and password confirmation do not match', 409)

        user = UserModel.find_by_username(args.get('username'))

        if user:
            return ResponseError('User with this username already exists', 409)

        hashed_password = UserModel.generate_hash(args.get('password'))

        new_user = UserModel(username=args.get('username'), password=hashed_password)
        new_user.save_to_db()

        return ResponseData({'access_token': user_summary.dump(new_user)})
