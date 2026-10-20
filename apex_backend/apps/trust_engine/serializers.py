from rest_framework import serializers
from .models import TrustScore, TrustScoreHistory


class TrustScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustScore
        fields = (
            'id', 'psp_consistency_score', 'cohort_performance_score',
            'vendor_rating_score', 'authenticity_confidence',
            'overall_merit_score', 'tier', 'last_calculated',
        )
        read_only_fields = fields


class TrustScoreHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustScoreHistory
        fields = (
            'id', 'overall_merit_score', 'psp_consistency_score',
            'cohort_performance_score', 'vendor_rating_score',
            'authenticity_confidence', 'reason', 'recorded_at',
        )
        read_only_fields = fields
