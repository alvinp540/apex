from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView,
    EmailVerifyView, MeView,
    PasswordResetView, PasswordResetConfirmView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('password/reset/', PasswordResetView.as_view()),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view()),
    path('email/verify/<str:token>/', EmailVerifyView.as_view()),
    path('me/', MeView.as_view()),
]
