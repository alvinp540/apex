from django.urls import path
from .views import (
    FundEscrowView, ReleaseEscrowView, DisputeEscrowView,
    EscrowDetailView, MpesaCallbackView, StripeWebhookView,
)

urlpatterns = [
    path('fund/', FundEscrowView.as_view()),
    path('release/<uuid:escrow_id>/', ReleaseEscrowView.as_view()),
    path('dispute/<uuid:escrow_id>/', DisputeEscrowView.as_view()),
    path('<uuid:escrow_id>/', EscrowDetailView.as_view()),
    path('mpesa/callback/', MpesaCallbackView.as_view()),
    path('stripe/webhook/', StripeWebhookView.as_view()),
]
