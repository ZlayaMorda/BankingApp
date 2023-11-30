import datetime
import jwt
from django.contrib.auth import get_user_model

from apps.authorization.forms import UserSignInForm
from banking.settings import SECRET_KEY
from django.http import HttpResponse
from django.template import loader

from utils.exceptions import AuthException, NotFound


class CustomJwt:
    @staticmethod
    def generate_jwt(user, days=0, minutes=5):  # TODO set in env time
        token_payload = {
            "user_uuid": str(user.user_uuid),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=days, minutes=minutes),
            "iat": datetime.datetime.utcnow(),
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def get_user_from_token(request):
        token = request.COOKIES.get("jwt_token")
        if token is None:  # TODO AUTH Exception
            raise AuthException("Authentication credentials were not provided")
        try:
            payload = jwt.decode(
                token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthException("expired token, please login again.")

        user = get_user_model().objects.filter(user_uuid=payload.get("user_uuid")).first()
        if user is None:
            raise NotFound("User not found")

        if not user.is_active:
            raise AuthException("User is inactive")

        return user

    @staticmethod
    def set_cookie_jwt(response, jwt_token, days=0, minutes=5):

        max_age = days * 24 * 60 * 60 + minutes * 60
        expires = datetime.datetime.strftime(
            datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
            "%a, %d-%b-%Y %H:%M:%S GMT",
        )
        response.set_cookie(  # TODO check envs
            "jwt_token",
            jwt_token,
            max_age=max_age,
            expires=expires,
            # domain=SESSION_COOKIE_DOMAIN,
            # secure=SESSION_COOKIE_SECURE,
        )
