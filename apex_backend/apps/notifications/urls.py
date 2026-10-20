from django.urls import path
from .views import ActivityNotificationView, NotificationListView, MarkReadView, MarkAllReadView, UnreadCountView

urlpatterns = [
    path('', NotificationListView.as_view()),
    path('<uuid:notif_id>/read/', MarkReadView.as_view()),
    path('read-all/', MarkAllReadView.as_view()),
    path('unread-count/', UnreadCountView.as_view()),
    path('activity/', ActivityNotificationView.as_view()),
]
