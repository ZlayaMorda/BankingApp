from django.contrib.auth.backends import BaseBackend
from apps.authorization.services.custom_jwt import CustomJwt
from apps.users.models import CustomUser


class JWTAuthBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        return CustomJwt().get_user_from_token(request)

    def get_user(self, user_uuid):
        try:
            return CustomUser.objects.get(pk=user_uuid)
        except:
            raise Exception("Not found")
