import smtplib
from flask import current_app


def send_confirmation_email(recipient, message):
    host = current_app.config.get('SMTP_HOST')
    port = current_app.config.get('SMTP_PORT')
    sender = current_app.config.get('SMTP_FROM')
    print(f'{host=}\n{port=}\n{sender=}\n{recipient=}')

    with smtplib.SMTP_SSL(
            host=current_app.config.get('SMTP_HOST'),
            port=current_app.config.get('SMTP_PORT')
    ) as smtp:
        smtp.ehlo()
        smtp.login(
            user=current_app.config.get('SMTP_USER'),
            password=current_app.config.get('SMTP_PASSWORD'),
        )

        smtp.sendmail(
            current_app.config.get('SMTP_FROM'),
            recipient,
            message.as_string()
        )
