import requests
import base64
from datetime import datetime
from django.conf import settings


def _get_access_token() -> str:
    url = (
        'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        if settings.MPESA_ENV == 'sandbox'
        else 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    )
    credentials = base64.b64encode(
        f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}".encode()
    ).decode()
    resp = requests.get(url, headers={'Authorization': f'Basic {credentials}'}, timeout=30)
    resp.raise_for_status()
    return resp.json()['access_token']


def _get_password() -> tuple[str, str]:
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    raw = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
    password = base64.b64encode(raw.encode()).decode()
    return password, timestamp


def stk_push(phone: str, amount: int, reference: str, description: str) -> dict:
    token = _get_access_token()
    password, timestamp = _get_password()

    base_url = (
        'https://sandbox.safaricom.co.ke'
        if settings.MPESA_ENV == 'sandbox'
        else 'https://api.safaricom.co.ke'
    )
    payload = {
        'BusinessShortCode': settings.MPESA_SHORTCODE,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone,
        'PartyB': settings.MPESA_SHORTCODE,
        'PhoneNumber': phone,
        'CallBackURL': settings.MPESA_CALLBACK_URL,
        'AccountReference': reference,
        'TransactionDesc': description,
    }
    resp = requests.post(
        f'{base_url}/mpesa/stkpush/v1/processrequest',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()
