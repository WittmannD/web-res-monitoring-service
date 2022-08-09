import smtplib
from flask import current_app


def send_confirmation_email(email, message):
    try:
        with smtplib.SMTP(
                host=current_app.config.get('SMTP_HOST'),
                port=current_app.config.get('SMTP_PORT')
        ) as smtp:

            smtp.starttls()
            smtp.login(
                user=current_app.config.get('SMTP_USER'),
                password=current_app.config.get('SMTP_PASSWORD'),
            )

            smtp.sendmail(
                current_app.config.get('SMTP_FROM'),
                email,
                message.as_string()
            )

    except smtplib.SMTPException as err:
        print(err)
