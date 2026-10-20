from django.urls import path
from .views import TriggerRouterView

urlpatterns = [
    path('trigger/', TriggerRouterView.as_view()),
]
