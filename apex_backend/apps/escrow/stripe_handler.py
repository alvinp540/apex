import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(amount_cents: int, currency: str, metadata: dict) -> dict:
    intent = stripe.PaymentIntent.create(
        amount=amount_cents,
        currency=currency.lower(),
        metadata=metadata,
        payment_method_types=['card'],
    )
    return {'client_secret': intent.client_secret, 'payment_intent_id': intent.id}


def confirm_payment_intent(payment_intent_id: str) -> bool:
    intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    return intent.status == 'succeeded'


def handle_webhook(payload: bytes, sig_header: str) -> stripe.Event:
    return stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )
