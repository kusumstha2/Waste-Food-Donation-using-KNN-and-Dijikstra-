from django.core.mail import send_mail
from django.conf import settings
import logging
from django.contrib.auth import get_user_model  

logger = logging.getLogger(__name__)
User = get_user_model()

def send_email_to_recipient(subject, message, recipient_id):
    try:
        recipient = User.objects.get(id=recipient_id, is_Recipient=True)  # Use the correct case for 'is_Recipient'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient.email],
            fail_silently=False,
        )
        logger.info(f"Email sent to {recipient.email}")
    except User.DoesNotExist:
        logger.error(f"Recipient with ID {recipient_id} not found or is not marked as a recipient")
    except Exception as e:
        logger.error(f"Error sending email: {e}")
