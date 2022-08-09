from flask import request
from flask_restful import Resource
from jwt import DecodeError, ExpiredSignatureError

from api.models import UserModel
from api.models.Schemas.UserSchema import user_summary
from api.utils.utils import ResponseData, token_required, verified_email_required


class UserApi(Resource):
    @staticmethod
    @token_required
    @verified_email_required
    def get(current_user: UserModel):
        return ResponseData(user_summary.dump(current_user))
