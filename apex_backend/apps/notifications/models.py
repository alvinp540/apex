from django.db import models
import uuid
from apps.accounts.models import User


class Notification(models.Model):
    TYPE_CHOICES = [
        ('opportunity', 'Opportunity'), ('ranking_change', 'Ranking Change'),
        ('score_update', 'Score Update'), ('payment', 'Payment'),
        ('assessment', 'Assessment'), ('system', 'System'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, db_index=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    action_url = models.CharField(max_length=500, blank=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
