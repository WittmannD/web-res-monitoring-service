from http import HTTPStatus

from flask import current_app
from flask_restful import Resource

from api.models.Schemas.TokensSchema import verification_token_summary
from api.models.UserModel import UserModel
from api.utils.email.confirmation_message import get_confirmation_message
from api.utils.email.send_confirmation_email import send_confirmation_email
from api.utils.utils import token_required, ResponseData, ApiError


class SendVerificationApi(Resource):
    @staticmethod
    @token_required
    def post(current_user: UserModel):

        if current_user.email_verified:
            raise ApiError('Email already verified', status=HTTPStatus.CONFLICT)

        token = verification_token_summary.dump(current_user)

        send_confirmation_email(
            current_user.email,
            get_confirmation_message(
                current_user.email,
                f'{current_app.config.get("PUBLIC_URL")}/auth/verification?token={token}'
            )
        )

        return ResponseData({}, status=HTTPStatus.NO_CONTENT)
