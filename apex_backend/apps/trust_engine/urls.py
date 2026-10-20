from django.urls import path
from .views import TrustScoreView, TrustScoreHistoryView, RecalculateTrustScoreView

urlpatterns = [
    path('score/', TrustScoreView.as_view()),
    path('score/history/', TrustScoreHistoryView.as_view()),
    path('recalculate/', RecalculateTrustScoreView.as_view()),
]
