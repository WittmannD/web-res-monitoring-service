from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app

from src.utils.email.confirmation_email_template import get_confirmation_email_template


def get_confirmation_message(email_to, confirmation_link):
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Email Verification'
    message['From'] = current_app.config.get('SMTP_FROM')
    message['To'] = email_to

    text = f'Please confirm your email address {confirmation_link}'
    html = get_confirmation_email_template(confirmation_link)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    message.attach(part1)
    message.attach(part2)
    return message
