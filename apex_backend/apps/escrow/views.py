from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from decimal import Decimal

from .models import EscrowPayment
from .serializers import EscrowPaymentSerializer, FundEscrowSerializer
from .mpesa import stk_push
from .stripe_handler import create_payment_intent, handle_webhook
from apps.vendor.models import VendorJob


class FundEscrowView(APIView):
    def post(self, request):
        serializer = FundEscrowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        job = get_object_or_404(VendorJob, id=data['job_id'], vendor=request.user, status='matched')

        if hasattr(job, 'escrow') and job.escrow.status == 'funded':
            return Response({'error': 'Escrow already funded.'}, status=status.HTTP_400_BAD_REQUEST)

        amount = job.budget_max
        fee = round(amount * Decimal(settings.PLATFORM_FEE_PERCENT) / 100, 2)
        net = amount - fee

        escrow, _ = EscrowPayment.objects.get_or_create(
            job=job,
            defaults={
                'vendor': request.user,
                'professional': job.assigned_professional,
                'amount': amount,
                'currency': job.currency,
                'platform_fee': fee,
                'net_payout': net,
                'provider': data['provider'],
            },
        )

        if data['provider'] == 'mpesa':
            phone = data.get('phone', '')
            result = stk_push(
                phone=phone,
                amount=int(amount),
                reference=str(job.id)[:12],
                description=f'APEX Escrow: {job.title[:20]}',
            )
            return Response({'mpesa': result, 'escrow_id': str(escrow.id)})

        # Stripe
        result = create_payment_intent(
            amount_cents=int(amount * 100),
            currency=job.currency,
            metadata={'escrow_id': str(escrow.id), 'job_id': str(job.id)},
        )
        return Response({'stripe': result, 'escrow_id': str(escrow.id)})


class ReleaseEscrowView(APIView):
    def post(self, request, escrow_id):
        escrow = get_object_or_404(
            EscrowPayment, id=escrow_id, vendor=request.user, status='funded'
        )
        escrow.status = 'released'
        escrow.released_at = timezone.now()
        escrow.save(update_fields=['status', 'released_at'])
        escrow.job.status = 'completed'
        escrow.job.save(update_fields=['status'])
        return Response({'message': 'Payment released to professional.'})


class DisputeEscrowView(APIView):
    def post(self, request, escrow_id):
        escrow = get_object_or_404(
            EscrowPayment, id=escrow_id, vendor=request.user, status='funded'
        )
        escrow.status = 'disputed'
        escrow.save(update_fields=['status'])
        return Response({'message': 'Dispute raised. Admin will review.'})


class EscrowDetailView(APIView):
    def get(self, request, escrow_id):
        escrow = EscrowPayment.objects.filter(
            id=escrow_id
        ).filter(
            vendor=request.user
        ).first() or get_object_or_404(EscrowPayment, id=escrow_id, professional=request.user)
        return Response(EscrowPaymentSerializer(escrow).data)


class MpesaCallbackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        body = request.data.get('Body', {})
        callback = body.get('stkCallback', {})
        result_code = callback.get('ResultCode')
        metadata = callback.get('CallbackMetadata', {}).get('Item', [])

        if result_code == 0:
            mpesa_ref = next(
                (i['Value'] for i in metadata if i['Name'] == 'MpesaReceiptNumber'), ''
            )
            # Match escrow by merchant request id if available
            escrow_ref = callback.get('AccountReference', '')
            try:
                job = VendorJob.objects.get(id=escrow_ref[:36])
                escrow = job.escrow
                escrow.status = 'funded'
                escrow.provider_transaction_id = mpesa_ref
                escrow.funded_at = timezone.now()
                escrow.save(update_fields=['status', 'provider_transaction_id', 'funded_at'])
            except Exception:
                pass
        return Response({'ResultCode': 0, 'ResultDesc': 'Accepted'})


class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        import stripe
        sig = request.META.get('HTTP_STRIPE_SIGNATURE', '')
        try:
            event = handle_webhook(request.body, sig)
        except stripe.error.SignatureVerificationError:
            return Response({'error': 'Invalid signature.'}, status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'payment_intent.succeeded':
            pi = event['data']['object']
            escrow_id = pi.get('metadata', {}).get('escrow_id')
            if escrow_id:
                try:
                    escrow = EscrowPayment.objects.get(id=escrow_id)
                    escrow.status = 'funded'
                    escrow.provider_transaction_id = pi['id']
                    escrow.funded_at = timezone.now()
                    escrow.save(update_fields=['status', 'provider_transaction_id', 'funded_at'])
                except EscrowPayment.DoesNotExist:
                    pass
        return Response({'received': True})
