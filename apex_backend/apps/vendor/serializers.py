from rest_framework import serializers
from .models import VendorJob, VendorRating


class VendorJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorJob
        fields = (
            'id', 'title', 'description', 'profession_required', 'skills_required',
            'budget_min', 'budget_max', 'currency', 'deadline', 'priority',
            'status', 'min_trust_score', 'evidence_urls', 'location_preference',
            'assigned_professional', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'status', 'assigned_professional', 'created_at', 'updated_at')


class VendorRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRating
        fields = (
            'id', 'quality_score', 'communication_score',
            'timeliness_score', 'overall_score', 'comment',
        )

    def validate(self, attrs):
        for field in ('quality_score', 'communication_score', 'timeliness_score'):
            if not (1 <= attrs[field] <= 5):
                raise serializers.ValidationError({field: 'Score must be between 1 and 5.'})
        attrs['overall_score'] = round(
            (attrs['quality_score'] + attrs['communication_score'] + attrs['timeliness_score']) / 3, 2
        )
        return attrs
