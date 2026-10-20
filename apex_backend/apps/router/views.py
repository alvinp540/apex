from rest_framework.views import APIView
from rest_framework.response import Response
from apps.accounts.permissions import IsAdmin
from .engine import route_job
from .serializers import RouteJobSerializer


class TriggerRouterView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = RouteJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        count = route_job(str(serializer.validated_data['job_id']))
        return Response({'matched': count})
