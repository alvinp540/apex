import requests
from django.conf import settings


def send_whatsapp(phone: str, message: str) -> bool:
    """Send a WhatsApp text through Meta Cloud API when configured."""
    access_token = getattr(settings, 'WHATSAPP_ACCESS_TOKEN', '')
    phone_number_id = getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', '')
    api_version = getattr(settings, 'WHATSAPP_API_VERSION', 'v20.0')
    if not phone or not access_token or not phone_number_id:
        return False

    url = f'https://graph.facebook.com/{api_version}/{phone_number_id}/messages'
    payload = {
        'messaging_product': 'whatsapp',
        'to': phone,
        'type': 'text',
        'text': {'preview_url': False, 'body': message},
    }
    try:
        response = requests.post(
            url,
            json=payload,
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=10,
        )
        return response.ok
    except requests.RequestException:
        return False
