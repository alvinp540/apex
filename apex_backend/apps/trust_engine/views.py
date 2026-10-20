from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import TrustScore, TrustScoreHistory
from .serializers import TrustScoreSerializer, TrustScoreHistorySerializer
from .engine import recalculate_trust_score
from apps.accounts.permissions import IsAdmin


class TrustScoreView(APIView):
    def get(self, request):
        ts = get_object_or_404(TrustScore, user=request.user)
        return Response(TrustScoreSerializer(ts).data)


class TrustScoreHistoryView(APIView):
    def get(self, request):
        history = TrustScoreHistory.objects.filter(
            user=request.user
        ).order_by('-recorded_at')[:50]
        return Response(TrustScoreHistorySerializer(history, many=True).data)


class RecalculateTrustScoreView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        ts = recalculate_trust_score(request.user, reason='Admin triggered recalculation')
        return Response(TrustScoreSerializer(ts).data)
