from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta

from apps.accounts.permissions import IsAdmin
from apps.accounts.models import User, Subscription
from apps.vendor.models import VendorJob, VendorRating
from apps.escrow.models import EscrowPayment
from apps.cohorts.models import AssessmentAttempt, CohortEnrollment
from apps.trust_engine.models import TrustScore
from apps.rankings.models import Ranking
from apps.rankings.serializers import RankingSerializer


class PlatformAnalyticsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        now = timezone.now()
        last_30 = now - timedelta(days=30)
        return Response({
            'total_users': User.objects.count(),
            'new_users_30d': User.objects.filter(created_at__gte=last_30).count(),
            'active_subscriptions': Subscription.objects.filter(status='active').count(),
            'total_jobs': VendorJob.objects.count(),
            'completed_jobs': VendorJob.objects.filter(status='completed').count(),
            'total_escrow_funded': EscrowPayment.objects.filter(
                status__in=['funded', 'released']
            ).aggregate(total=Sum('amount'))['total'] or 0,
            'total_assessments_taken': AssessmentAttempt.objects.filter(status='graded').count(),
            'flagged_attempts': AssessmentAttempt.objects.filter(is_flagged=True).count(),
            'avg_merit_score': TrustScore.objects.aggregate(avg=Avg('overall_merit_score'))['avg'] or 0,
            'tier_breakdown': {
                row['tier']: row['count']
                for row in TrustScore.objects.values('tier').annotate(count=Count('id'))
            },
        })


class PublicPlatformStatsView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        total_jobs = VendorJob.objects.count()
        completed_jobs = VendorJob.objects.filter(status='completed').count()
        earned = EscrowPayment.objects.filter(status='released').aggregate(total=Sum('amount'))['total'] or 0
        return Response({
            'active_professionals': User.objects.filter(role='professional', is_active=True).count(),
            'real_opportunities': total_jobs,
            'successful_jobs_percent': round((completed_jobs / total_jobs) * 100) if total_jobs else 0,
            'verified_vendors': User.objects.filter(role='vendor', is_active=True).count(),
            'earned_amount': earned,
            'currency': 'KES',
            'average_merit_score': round(float(TrustScore.objects.aggregate(avg=Avg('overall_merit_score'))['avg'] or 0)),
            'top_professionals': RankingSerializer(
                Ranking.objects.select_related('user__profile', 'user__trust_score').order_by('global_rank')[:5],
                many=True,
            ).data,
            'recent_opportunities': list(
                VendorJob.objects.filter(status='open').order_by('-created_at').values(
                    'id', 'title', 'profession_required', 'budget_max', 'currency', 'priority'
                )[:3]
            ),
        })


class ProfessionalAnalyticsView(APIView):
    def get(self, request):
        user = request.user
        attempts = AssessmentAttempt.objects.filter(user=user, status='graded')
        return Response({
            'total_assessments': attempts.count(),
            'avg_score': attempts.aggregate(avg=Avg('score'))['avg'] or 0,
            'flagged_attempts': attempts.filter(is_flagged=True).count(),
            'opportunities_received': user.opportunities.count(),
            'jobs_completed': user.assigned_jobs.filter(status='completed').count(),
            'avg_vendor_rating': VendorRating.objects.filter(
                professional=user
            ).aggregate(avg=Avg('overall_score'))['avg'] or 0,
        })


class VendorAnalyticsView(APIView):
    def get(self, request):
        user = request.user
        jobs = VendorJob.objects.filter(vendor=user)
        return Response({
            'total_jobs_posted': jobs.count(),
            'jobs_by_status': {
                row['status']: row['count']
                for row in jobs.values('status').annotate(count=Count('id'))
            },
            'total_spent': EscrowPayment.objects.filter(
                vendor=user, status__in=['funded', 'released']
            ).aggregate(total=Sum('amount'))['total'] or 0,
            'avg_rating_given': VendorRating.objects.filter(
                vendor=user
            ).aggregate(avg=Avg('overall_score'))['avg'] or 0,
        })
