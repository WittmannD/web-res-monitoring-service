from http import HTTPStatus

from flask import current_app
from flask_restful import Resource

from src.models.Schemas.TokensSchema import verification_token_summary
from src.models.UserModel import UserModel
from src.utils.email.confirmation_message import get_confirmation_message
from src.utils.email.send_confirmation_email import send_confirmation_email
from src.utils.utils import token_required, ResponseData, ApiError


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
