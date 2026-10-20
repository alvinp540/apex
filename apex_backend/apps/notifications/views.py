from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Notification
from .utils import send_notification
from .serializers import NotificationSerializer
from utils.pagination import StandardResultsPagination


class NotificationListView(APIView):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(notifications, request)
        return paginator.get_paginated_response(NotificationSerializer(page, many=True).data)


class MarkReadView(APIView):
    def patch(self, request, notif_id):
        notif = get_object_or_404(Notification, id=notif_id, user=request.user)
        notif.is_read = True
        notif.save(update_fields=['is_read'])
        return Response({'status': 'ok'})


class MarkAllReadView(APIView):
    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'ok'})


class UnreadCountView(APIView):
    def get(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})


class ActivityNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = str(request.data.get('title', '')).strip()
        message = str(request.data.get('message', '')).strip()
        if not title or not message:
            return Response({'error': 'Notification title and message are required.'}, status=400)
        notification_type = request.data.get('notification_type', 'system')
        allowed_types = {choice[0] for choice in Notification.TYPE_CHOICES}
        if notification_type not in allowed_types:
            notification_type = 'system'
        notification = send_notification(
            user=request.user,
            notification_type=notification_type,
            title=title,
            message=message,
            action_url=str(request.data.get('action_url', '')).strip(),
            metadata=request.data.get('metadata') or {},
        )
        return Response(NotificationSerializer(notification).data, status=201)
