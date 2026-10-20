from django.db import models
import uuid
from apps.accounts.models import User


class Profile(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=200)
    headline = models.CharField(max_length=300, blank=True)
    bio = models.TextField(blank=True)
    profession = models.CharField(max_length=100, db_index=True)
    skills = models.JSONField(default=list)
    location = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True, db_index=True)
    avatar_url = models.URLField(blank=True, null=True)
    availability = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES, default='offline', db_index=True
    )
    is_online = models.BooleanField(default=False, db_index=True)
    last_seen_at = models.DateTimeField(null=True, blank=True, db_index=True)
    years_experience = models.PositiveSmallIntegerField(default=0)
    portfolio_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    highlights = models.JSONField(default=list)
    show_whatsapp = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'
        indexes = [
            models.Index(fields=['profession', 'availability']),
            models.Index(fields=['country']),
        ]

    def __str__(self):
        return self.full_name


class MentorOrganization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mentor_organizations'


class Mentor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    organization = models.ForeignKey(MentorOrganization, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentors')
    bio = models.TextField(blank=True)
    skills = models.JSONField(default=list)
    tier = models.CharField(max_length=64, blank=True)
    consistency_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mentors'

    def __str__(self):
        return getattr(self.user, 'username', str(self.id))
