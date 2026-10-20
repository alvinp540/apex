from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import FraudLog, AuditLog
from .serializers import FraudLogSerializer, AuditLogSerializer
from apps.accounts.permissions import IsAdmin
from apps.accounts.serializers import UserSerializer
from apps.accounts.models import User
from utils.pagination import StandardResultsPagination


class AdminUserListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        users = User.objects.all().order_by('-created_at')
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(users, request)
        return paginator.get_paginated_response(UserSerializer(page, many=True).data)


class AdminUserStatusView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        is_active = request.data.get('is_active')
        if is_active is not None:
            user.is_active = is_active
            user.save(update_fields=['is_active'])
        return Response(UserSerializer(user).data)


class FraudLogListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        logs = FraudLog.objects.order_by('-created_at')
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(logs, request)
        return paginator.get_paginated_response(FraudLogSerializer(page, many=True).data)


class FraudLogResolveView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, log_id):
        log = get_object_or_404(FraudLog, id=log_id)
        log.is_resolved = True
        log.save(update_fields=['is_resolved'])
        return Response({'status': 'resolved'})


class AuditLogListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        logs = AuditLog.objects.order_by('-created_at')
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(logs, request)
        return paginator.get_paginated_response(AuditLogSerializer(page, many=True).data)


class AdminEscrowListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        from apps.escrow.models import EscrowPayment
        from apps.escrow.serializers import EscrowPaymentSerializer
        escrows = EscrowPayment.objects.all().order_by('-created_at')
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(escrows, request)
        return paginator.get_paginated_response(EscrowPaymentSerializer(page, many=True).data)


class AdminRecalculateRankingsView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        from apps.rankings.tasks import recalculate_all_rankings
        recalculate_all_rankings.delay()
        return Response({'message': 'Global ranking recalculation started.'})
