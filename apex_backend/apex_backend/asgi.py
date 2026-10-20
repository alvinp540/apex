import os

default_settings = (
    'apex_backend.settings.production'
    if os.environ.get('VERCEL')
    else 'apex_backend.settings.development'
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', default_settings)

from django.core.asgi import get_asgi_application

django_asgi_application = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.notifications.middleware import JWTQueryAuthMiddleware
from apps.notifications.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi_application,
    'websocket': AuthMiddlewareStack(
        JWTQueryAuthMiddleware(URLRouter(websocket_urlpatterns))
    ),
})
