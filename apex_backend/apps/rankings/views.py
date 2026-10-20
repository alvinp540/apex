from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Ranking
from .serializers import RankingSerializer
from utils.pagination import StandardResultsPagination


class GlobalLeaderboardView(APIView):
    def get(self, request):
        rankings = Ranking.objects.select_related(
            'user__profile', 'user__trust_score'
        ).order_by('global_rank')
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(rankings, request)
        return paginator.get_paginated_response(RankingSerializer(page, many=True).data)


class ProfessionLeaderboardView(APIView):
    def get(self, request, profession):
        rankings = Ranking.objects.filter(
            profession__iexact=profession
        ).select_related('user__profile', 'user__trust_score').order_by('profession_rank')
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(rankings, request)
        return paginator.get_paginated_response(RankingSerializer(page, many=True).data)


class CountryLeaderboardView(APIView):
    def get(self, request, country_code):
        rankings = Ranking.objects.filter(
            user__profile__country__iexact=country_code
        ).select_related('user__profile', 'user__trust_score').order_by('country_rank')
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(rankings, request)
        return paginator.get_paginated_response(RankingSerializer(page, many=True).data)


class MyRankingView(APIView):
    def get(self, request):
        ranking = get_object_or_404(Ranking, user=request.user)
        return Response(RankingSerializer(ranking).data)
