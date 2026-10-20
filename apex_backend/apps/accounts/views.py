from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
import uuid
from django.conf import settings

from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer,
)
from .models import User


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.email_verification_token = str(uuid.uuid4())

        if settings.EMAIL_HOST_USER:
            user.save(update_fields=['email_verification_token'])
            try:
                from .tasks import send_verification_email
                send_verification_email.delay(str(user.id))
            except Exception:
                pass
        else:
            user.is_email_verified = True
            user.email_verification_token = None
            user.save(update_fields=['is_email_verified', 'email_verification_token'])

        return Response(
            {'message': 'Registration successful. Check your email to verify your account.'},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )
        if not user:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_email_verified and settings.EMAIL_HOST_USER:
            return Response({'error': 'Email not verified.'}, status=status.HTTP_403_FORBIDDEN)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        })


class LogoutView(APIView):
    def post(self, request):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            return Response({'message': 'Logged out.'}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerifyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        user = User.objects.filter(email_verification_token=token).first()
        if not user:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_email_verified = True
        user.email_verification_token = None
        user.save(update_fields=['is_email_verified', 'email_verification_token'])
        return Response({'message': 'Email verified successfully.'})


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data['email']).first()
        if user:
            token = get_random_string(64)
            user.email_verification_token = token
            user.save(update_fields=['email_verification_token'])
            try:
                from .tasks import send_password_reset_email
                send_password_reset_email.delay(str(user.id), token)
            except Exception:
                pass
        return Response({'message': 'If that email exists, a reset link has been sent.'})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(
            email_verification_token=serializer.validated_data['token']
        ).first()
        if not user:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.email_verification_token = None
        user.save(update_fields=['password', 'email_verification_token'])
        return Response({'message': 'Password reset successfully.'})
