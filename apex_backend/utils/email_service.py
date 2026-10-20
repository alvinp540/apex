from django.core.mail import send_mail
from django.conf import settings


def send_email(to: str, subject: str, message: str) -> bool:
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to],
            fail_silently=False,
        )
        return True
    except Exception:
        return False
