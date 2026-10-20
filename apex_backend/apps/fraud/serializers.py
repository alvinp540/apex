from rest_framework import serializers
from .models import FraudLog, AuditLog


class FraudLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudLog
        fields = (
            'id', 'user', 'event_type', 'severity', 'description',
            'ip_address', 'metadata', 'is_resolved', 'created_at',
        )
        read_only_fields = fields


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = (
            'id', 'user', 'action', 'model_name',
            'object_id', 'changes', 'ip_address', 'created_at',
        )
        read_only_fields = fields
