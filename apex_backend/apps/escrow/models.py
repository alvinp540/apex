from django.db import models
import uuid
from apps.accounts.models import User
from apps.vendor.models import VendorJob


class EscrowPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('funded', 'Funded'), ('released', 'Released'),
        ('disputed', 'Disputed'), ('refunded', 'Refunded'),
    ]
    PROVIDER_CHOICES = [('stripe', 'Stripe'), ('mpesa', 'M-Pesa')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.OneToOneField(VendorJob, on_delete=models.CASCADE, related_name='escrow')
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='escrow_funded')
    professional = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='escrow_earned'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=5, default='KES')
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_payout = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    provider = models.CharField(max_length=10, choices=PROVIDER_CHOICES)
    provider_transaction_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    funded_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'escrow_payments'
        indexes = [models.Index(fields=['status'])]
