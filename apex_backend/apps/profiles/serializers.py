from rest_framework import serializers
import hashlib
import hmac
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Profile
from .models import Mentor, MentorOrganization
from apps.accounts.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    is_online = serializers.SerializerMethodField()
    last_seen_at = serializers.DateTimeField(read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', required=False, allow_blank=True)
    whatsapp_hashed_number = serializers.SerializerMethodField()
    whatsapp_chat_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'id', 'email', 'role', 'full_name', 'headline', 'bio',
            'profession', 'skills', 'location', 'country', 'avatar_url', 'phone_number',
            'availability', 'years_experience', 'portfolio_url', 'linkedin_url',
            'highlights', 'show_whatsapp',
            'is_online', 'last_seen_at',
            'whatsapp_hashed_number', 'whatsapp_chat_url',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'email', 'role', 'created_at', 'updated_at')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        phone_number = user_data.get('phone_number')
        if phone_number is not None:
            instance.user.phone_number = phone_number
            instance.user.save(update_fields=['phone_number', 'updated_at'])
        return super().update(instance, validated_data)

    def get_whatsapp_hashed_number(self, obj):
        phone = (obj.user.phone_number or '').strip()
        if not phone:
            return None
        digest = hmac.new(
            str(settings.SECRET_KEY).encode(),
            phone.encode(),
            hashlib.sha256,
        ).hexdigest()
        return f'APEX-{digest[:12].upper()}'

    def get_is_online(self, obj):
        return bool(obj.is_online and obj.last_seen_at and obj.last_seen_at >= timezone.now() - timedelta(seconds=90))

    def get_whatsapp_chat_url(self, obj):
        phone = ''.join(char for char in (obj.user.phone_number or '') if char.isdigit())
        return f'https://wa.me/{phone}' if phone else None


class PublicProfileSerializer(serializers.ModelSerializer):
    is_online = serializers.SerializerMethodField()
    whatsapp_chat_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'id', 'full_name', 'headline', 'profession', 'skills',
            'location', 'country', 'avatar_url', 'availability',
            'years_experience', 'portfolio_url', 'linkedin_url',
            'highlights', 'is_online', 'whatsapp_chat_url',
        )

    def get_is_online(self, obj):
        return bool(obj.is_online and obj.last_seen_at and obj.last_seen_at >= timezone.now() - timedelta(seconds=90))

    def get_whatsapp_chat_url(self, obj):
        if not obj.show_whatsapp:
            return None
        phone = ''.join(char for char in (obj.user.phone_number or '') if char.isdigit())
        return f'https://wa.me/{phone}' if phone else None


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('availability',)


class MentorOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorOrganization
        fields = ('id', 'name', 'description')


class MentorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    organization = MentorOrganizationSerializer(read_only=True)

    class Meta:
        model = Mentor
        fields = ('id', 'user', 'organization', 'bio', 'skills', 'tier', 'consistency_score')
