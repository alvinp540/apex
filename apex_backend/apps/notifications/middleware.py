from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError


class JWTQueryAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode('utf-8', errors='replace')
        token = parse_qs(query_string).get('token', [None])[0]
        if token:
            scope = dict(scope)
            authentication = JWTAuthentication()
            try:
                validated_token = authentication.get_validated_token(token)
                scope['user'] = await database_sync_to_async(authentication.get_user)(
                    validated_token
                )
            except (AuthenticationFailed, TokenError):
                scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)
