from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase
from rest_framework.exceptions import AuthenticationFailed

from apps.notifications.middleware import JWTQueryAuthMiddleware


class JwtQueryAuthMiddlewareTests(SimpleTestCase):
    async def invoke_middleware(self, query_string, initial_user=None):
        captured_users = []

        async def app(scope, receive, send):
            captured_users.append(scope.get('user'))

        async def receive():
            return {}

        async def send(message):
            return None

        scope = {'type': 'websocket', 'query_string': query_string}
        if initial_user is not None:
            scope['user'] = initial_user

        await JWTQueryAuthMiddleware(app)(scope, receive, send)
        return captured_users[0]

    async def test_valid_query_token_authenticates_websocket_user(self):
        authenticated_user = object()
        with (
            patch(
                'apps.notifications.middleware.JWTAuthentication.get_validated_token',
                return_value=object(),
            ),
            patch(
                'apps.notifications.middleware.JWTAuthentication.get_user',
                return_value=authenticated_user,
            ),
        ):
            user = await self.invoke_middleware(b'token=valid-access-token')

        self.assertIs(user, authenticated_user)

    async def test_invalid_query_token_becomes_anonymous(self):
        with patch(
            'apps.notifications.middleware.JWTAuthentication.get_validated_token',
            side_effect=AuthenticationFailed('Invalid token'),
        ):
            user = await self.invoke_middleware(b'token=invalid-access-token')

        self.assertIsInstance(user, AnonymousUser)

    async def test_missing_token_preserves_session_user(self):
        session_user = object()
        user = await self.invoke_middleware(b'', initial_user=session_user)

        self.assertIs(user, session_user)
