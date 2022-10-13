from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

from api.models import Token


User = get_user_model()


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token is not None:
            try:
                user = Token.objects.get(token=token).user
                return (user, None)
            except Token.DoesNotExist:
                raise exceptions.AuthenticationFailed('No such user or token is invalid')
        return None