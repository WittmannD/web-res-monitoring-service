from http import HTTPStatus

from flask_restful import Resource

from api.models.Schemas.TokensSchema import VerificationTokenSchema
from api.models.UserModel import UserModel
from api.utils.utils import token_required, ResponseData, ApiError


class EmailVerificationApi(Resource):
    @staticmethod
    @token_required
    @VerificationTokenSchema.validate_fields(location='query')
    def post(current_user: UserModel, args):
        user = UserModel.find_by_id(args.get('id'))

        if user is None or args.get('token_type') != 'VERIFICATION_TOKEN':
            raise ApiError('Valid access token is missing', status=HTTPStatus.UNAUTHORIZED)

        if current_user.id != user.id:
            raise ApiError('Access denied', status=HTTPStatus.FORBIDDEN)

        if user.email_verified:
            raise ApiError('Email already verified', status=HTTPStatus.CONFLICT)

        user.email_verified = True
        user.save_to_db()

        return ResponseData({}, HTTPStatus.NO_CONTENT)
