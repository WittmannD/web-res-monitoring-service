from flask_restful import Resource

from api.models.Schemas.UserSchema import UserSchema, user_summary
from api.models.UserModel import UserModel
from api.utils.utils import ResponseError, ResponseData


class LoginApi(Resource):
    @staticmethod
    @UserSchema.validate_fields(location="json")
    def post(args):
        user = UserModel.find_by_username(args.get('username'))

        if user and UserModel.verify_hash(user.password, args.get('password')):
            return ResponseData({'access_token': user_summary.dump(user)})

        else:
            return ResponseError('Incorrect username or password', 401)
