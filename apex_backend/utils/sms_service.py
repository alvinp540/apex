import requests
from django.conf import settings


def send_sms(phone: str, message: str) -> bool:
    """Placeholder — swap in Africa's Talking or similar."""
    try:
        # Example: Africa's Talking
        resp = requests.post(
            'https://api.africastalking.com/version1/messaging',
            data={'username': 'sandbox', 'to': phone, 'message': message},
            headers={'apiKey': getattr(settings, 'AT_API_KEY', ''), 'Accept': 'application/json'},
            timeout=10,
        )
        return resp.status_code == 201
    except Exception:
        return False
