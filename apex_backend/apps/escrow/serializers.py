from rest_framework import serializers
from .models import EscrowPayment


class EscrowPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscrowPayment
        fields = (
            'id', 'job', 'vendor', 'professional', 'amount', 'currency',
            'platform_fee', 'net_payout', 'provider', 'provider_transaction_id',
            'status', 'funded_at', 'released_at', 'created_at',
        )
        read_only_fields = (
            'id', 'vendor', 'platform_fee', 'net_payout',
            'provider_transaction_id', 'status', 'funded_at', 'released_at', 'created_at',
        )


class FundEscrowSerializer(serializers.Serializer):
    job_id = serializers.UUIDField()
    provider = serializers.ChoiceField(choices=['stripe', 'mpesa'])
    phone = serializers.CharField(required=False)         # M-Pesa only
    payment_intent_id = serializers.CharField(required=False)  # Stripe only
