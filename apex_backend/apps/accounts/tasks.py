from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_verification_email(user_id):
    from apps.accounts.models import User
    try:
        user = User.objects.get(id=user_id)
        verify_url = (
            f"{settings.FRONTEND_URL}/verify-email/{user.email_verification_token}"
        )
        send_mail(
            subject='Verify your APEX account',
            message=f'Click to verify your email: {verify_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        pass


@shared_task
def send_password_reset_email(user_id, token):
    from apps.accounts.models import User
    try:
        user = User.objects.get(id=user_id)
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
        send_mail(
            subject='Reset your APEX password',
            message=f'Click to reset your password: {reset_url}\nLink expires in 1 hour.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        pass
