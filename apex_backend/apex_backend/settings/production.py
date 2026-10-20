from .base import *
import os

DEBUG = False

if os.environ.get('VERCEL') and not os.environ.get('DJANGO_SECRET_KEY'):
    from django.core.exceptions import ImproperlyConfigured

    raise ImproperlyConfigured('Set DJANGO_SECRET_KEY in the Vercel backend project environment.')


def _env_list(name):
    return [value.strip() for value in os.environ.get(name, '').split(',') if value.strip()]


def _vercel_hosts():
    hosts = []
    for name in ('VERCEL_URL', 'VERCEL_PROJECT_PRODUCTION_URL'):
        value = os.environ.get(name, '').strip()
        if value:
            hosts.append(value.split('://')[-1].split('/')[0].split(':')[0])
    return hosts


ALLOWED_HOSTS = list(dict.fromkeys(_env_list('ALLOWED_HOSTS') + _vercel_hosts()))
CORS_ALLOWED_ORIGINS = _env_list('CORS_ALLOWED_ORIGINS')
CSRF_TRUSTED_ORIGINS = _env_list('CSRF_TRUSTED_ORIGINS')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
