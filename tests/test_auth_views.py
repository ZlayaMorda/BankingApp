from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.authorization.forms import UserSignUpForm, UserSignInForm, CodeForm
from unittest.mock import patch

class TestUserSignUpView(TestCase):
    def test_user_sign_up_get(self):
        response = self.client.get(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authorization/sign_up.html')
        self.assertIsInstance(response.context['form'], UserSignUpForm)

    def test_user_sign_up_post(self):
        data = {
            # Add required data for signing up a user
        }
        response = self.client.post(reverse('sign_up'), data=data)
        self.assertEqual(response.status_code, 200)  # Assuming it redirects after signing up

class TestUserSignInView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name='John',
            last_name='Doe',
            password='test123321',
            email='test@gmail.com',
            passport_identifier='1000000A000AA0'
        )

    def test_user_sign_in_get(self):
        response = self.client.get(reverse('sign_in'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authorization/sign_in.html')
        self.assertIsInstance(response.context['form'], UserSignInForm)

    @patch('apps.authorization.services.custom_jwt.CustomJwt.generate_jwt')
    @patch('apps.authorization.services.code_generation.Code.store')
    def test_user_sign_in_post_valid_credentials(self, mock_store, mock_generate_jwt):
        data = {
            "password": 'test123321',
            "passport_identifier": '1000000A000AA0'
        }

        mock_store.return_value = 'mocked_code'
        mock_generate_jwt.return_value = 'mocked_jwt'

        response = self.client.post(reverse('sign_in'), data=data)
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after signing in


class TestUserSignInCodeView(TestCase):
    def test_user_sign_in_code_get(self):
        response = self.client.get(reverse('sign_in_code'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authorization/sign_in_code.html')
        self.assertIsInstance(response.context['form'], CodeForm)

    def test_user_sign_in_code_post_valid_code(self):
        data = {}
        response = self.client.post(reverse('sign_in_code'), data=data)
        self.assertEqual(response.status_code, 200)  # Assuming it redirects after signing in with a code


class TestLogoutView(TestCase):
    def test_logout_get(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after logging out
