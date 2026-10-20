from rest_framework import serializers


class RouteJobSerializer(serializers.Serializer):
    job_id = serializers.UUIDField()
