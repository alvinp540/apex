from django.db import models
import uuid
from apps.accounts.models import User


class FraudLog(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fraud_logs')
    event_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, db_index=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True)
    metadata = models.JSONField(default=dict)
    is_resolved = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'fraud_logs'


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=200)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    changes = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'audit_logs'


class Opportunity(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('assigned', 'Assigned'), ('expired', 'Expired')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey('vendor.VendorJob', on_delete=models.CASCADE, related_name='opportunities')
    professional = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities')
    router_score = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    notified_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'opportunities'
