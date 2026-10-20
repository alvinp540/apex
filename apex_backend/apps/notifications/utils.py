from .models import Notification


def send_notification(user, notification_type: str, title: str, message: str,
                      action_url: str = '', metadata: dict = None):
    notif = Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        action_url=action_url,
        metadata=metadata or {},
    )
    # Push via WebSocket
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    channel_layer = get_channel_layer()
    group_name = f'notifications_{user.id}'
    try:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'notification_message',
                'notification': {
                    'id': str(notif.id),
                    'notification_type': notif.notification_type,
                    'title': notif.title,
                    'message': notif.message,
                    'action_url': notif.action_url,
                    'created_at': notif.created_at.isoformat(),
                },
            },
        )
    except Exception:
        pass  # WebSocket push is best-effort

    # WhatsApp delivery is best-effort; the in-app notification remains canonical.
    try:
        from utils.whatsapp_service import send_whatsapp
        send_whatsapp(getattr(user, 'phone_number', '') or '', f'{title}\n\n{message}')
    except Exception:
        pass
    return notif
