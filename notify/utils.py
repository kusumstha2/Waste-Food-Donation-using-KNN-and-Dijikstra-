from django.core.mail import send_mail
from django.conf import settings

def send_email_to_recipient(subject, message, recipient_email):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,

            [recipient_email],
        )
    except Exception as e:
        raise Exception(f"Error sending email: {e}")