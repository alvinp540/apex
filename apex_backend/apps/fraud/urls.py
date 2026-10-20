from django.urls import path
from .views import (
    AdminUserListView, AdminUserStatusView,
    FraudLogListView, FraudLogResolveView,
    AuditLogListView, AdminEscrowListView, AdminRecalculateRankingsView,
)

urlpatterns = [
    path('users/', AdminUserListView.as_view()),
    path('users/<uuid:user_id>/status/', AdminUserStatusView.as_view()),
    path('fraud-logs/', FraudLogListView.as_view()),
    path('fraud-logs/<uuid:log_id>/resolve/', FraudLogResolveView.as_view()),
    path('audit-logs/', AuditLogListView.as_view()),
    path('escrow/', AdminEscrowListView.as_view()),
    path('rankings/recalculate/', AdminRecalculateRankingsView.as_view()),
]
