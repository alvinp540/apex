from django.db import models
import uuid
from apps.accounts.models import User


class VendorJob(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'), ('open', 'Open'), ('matched', 'Matched'),
        ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    profession_required = models.CharField(max_length=100, db_index=True)
    skills_required = models.JSONField(default=list)
    budget_min = models.DecimalField(max_digits=12, decimal_places=2)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=5, default='KES')
    deadline = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    min_trust_score = models.FloatField(default=50.0)
    evidence_urls = models.JSONField(default=list)
    location_preference = models.CharField(max_length=200, blank=True)
    assigned_professional = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_jobs'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vendor_jobs'
        indexes = [models.Index(fields=['profession_required', 'status'])]


class VendorRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    professional = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_ratings')
    job = models.OneToOneField(VendorJob, on_delete=models.CASCADE, related_name='rating')
    quality_score = models.PositiveSmallIntegerField()
    communication_score = models.PositiveSmallIntegerField()
    timeliness_score = models.PositiveSmallIntegerField()
    overall_score = models.FloatField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vendor_ratings'
