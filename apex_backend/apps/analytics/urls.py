from django.urls import path
from .views import PlatformAnalyticsView, PublicPlatformStatsView, ProfessionalAnalyticsView, VendorAnalyticsView

urlpatterns = [
    path('public/', PublicPlatformStatsView.as_view()),
    path('platform/', PlatformAnalyticsView.as_view()),
    path('professional/me/', ProfessionalAnalyticsView.as_view()),
    path('vendor/me/', VendorAnalyticsView.as_view()),
]
