from django.db import models
import uuid
from apps.accounts.models import User


class TrustScore(models.Model):
    TIER_CHOICES = [
        ('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold'),
        ('platinum', 'Platinum'), ('apex', 'APEX'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trust_score')
    psp_consistency_score = models.FloatField(default=0.0)
    cohort_performance_score = models.FloatField(default=0.0)
    vendor_rating_score = models.FloatField(default=0.0)
    authenticity_confidence = models.FloatField(default=0.0)
    overall_merit_score = models.FloatField(default=0.0, db_index=True)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='bronze', db_index=True)
    last_calculated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'trust_scores'
        indexes = [models.Index(fields=['overall_merit_score'])]


class TrustScoreHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='score_history')
    overall_merit_score = models.FloatField()
    psp_consistency_score = models.FloatField()
    cohort_performance_score = models.FloatField()
    vendor_rating_score = models.FloatField()
    authenticity_confidence = models.FloatField()
    reason = models.CharField(max_length=255)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'trust_score_history'
        indexes = [models.Index(fields=['user', 'recorded_at'])]
