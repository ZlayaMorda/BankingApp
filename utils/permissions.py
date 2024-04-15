from django.contrib.auth.models import AnonymousUser

from utils.exceptions import AuthException


def logged_in(function):
    def inner(self, request, *args, **kwargs):
        if request.user is AnonymousUser:
            raise AuthException()
        else:
            return function(self, request, *args, **kwargs)
    return inner
