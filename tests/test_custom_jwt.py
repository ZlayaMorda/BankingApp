import datetime
import jwt
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from banking.settings import SECRET_KEY, EXPIRE_MINUTES, EXPIRE_DAYS
from utils.exceptions import AuthException, NotFound
from django.contrib.auth.models import AnonymousUser
from apps.authorization.services.custom_jwt import CustomJwt

class TestCustomJwt(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name='John',
            last_name='Doe',
            password='test123321',
            email='test@gmail.com',
            passport_identifier='1000000A000AA0'
        )

    def test_generate_jwt(self):
        token = CustomJwt.generate_jwt(self.user, 10, 10)
        self.assertIsInstance(token, str)

        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        self.assertEqual(decoded['user_uuid'], str(self.user.user_uuid))

    def test_get_user_from_token(self):
        token = jwt.encode({'user_uuid': str(self.user.user_uuid)}, SECRET_KEY, algorithm="HS256")

        request = HttpRequest()
        request.COOKIES['jwt_token'] = token

        user = CustomJwt.get_user_from_token(request)
        self.assertEqual(user, self.user)

        # Test scenarios

        request.COOKIES['jwt_token'] = None
        anonymous_user= CustomJwt.get_user_from_token(request)
        self.assertEqual(anonymous_user, AnonymousUser)

        token_payload = {
            'user_uuid': str(self.user.user_uuid),
            "exp": datetime.datetime.utcnow() - datetime.timedelta(seconds=1),
            "iat": datetime.datetime.utcnow(),
        }

        with self.assertRaises(AuthException):
            expired_token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256", )
            request.COOKIES['jwt_token'] = expired_token
            CustomJwt.get_user_from_token(request)

        with self.assertRaises(NotFound):
            invalid_user_token = jwt.encode({'user_uuid': '9fe8e820-870c-4eed-9a8a-1617b69ed812'}, SECRET_KEY, algorithm="HS256")
            request.COOKIES['jwt_token'] = invalid_user_token
            CustomJwt.get_user_from_token(request)

    def test_set_cookie_jwt(self):
        response = HttpResponse()
        jwt_token = jwt.encode({'user_uuid': str(self.user.user_uuid)}, SECRET_KEY, algorithm="HS256")
        CustomJwt.set_cookie_jwt(response, jwt_token)

        self.assertIn('jwt_token', response.cookies)
        cookie = response.cookies['jwt_token']
        self.assertEqual(cookie.value, jwt_token)
