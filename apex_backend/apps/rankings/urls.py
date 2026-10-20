from django.urls import path
from .views import (
    GlobalLeaderboardView, ProfessionLeaderboardView,
    CountryLeaderboardView, MyRankingView,
)

urlpatterns = [
    path('global/', GlobalLeaderboardView.as_view()),
    path('profession/<str:profession>/', ProfessionLeaderboardView.as_view()),
    path('country/<str:country_code>/', CountryLeaderboardView.as_view()),
    path('me/', MyRankingView.as_view()),
]
