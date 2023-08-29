from flask_restful import Resource

from src.models.UserModel import UserModel
from src.models.Schemas.UserSchema import user_summary
from src.utils.utils import ResponseData, token_required, verified_email_required


class UserApi(Resource):
    @staticmethod
    @token_required
    def get(current_user: UserModel):
        return ResponseData(user_summary.dump(current_user))
