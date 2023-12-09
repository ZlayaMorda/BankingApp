from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from apps.account.models import Account
from apps.account.views import (
    AccountDetailView,
    AccountListView,
    AccountCreateView,
    AccountDeleteView,
    AccountTransferView)
from apps.account.services.account_service import AccountService
from apps.account.forms import AccountCreateForm

User = get_user_model()

class TestAccountViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(first_name='John', last_name='Doe', password='test123321', email='test@gmail.com', passport_identifier='1000000A000AA0')
        self.account_service = AccountService()

    def test_account_list_view(self):
        request = self.factory.get('/accounts/')
        request.user = self.user

        account_list_view = AccountListView()
        response = account_list_view.get(request)

        self.assertEqual(response.status_code, 200)

    def test_account_create_view(self):
        request = self.factory.post('/account/create/', {'currency': 'USD'})
        request.user = self.user

        account_create_view = AccountCreateView()
        response = account_create_view.post(request)

        self.assertEqual(response.status_code, 302)  # Redirects to 'account_list'

    def test_account_detail_view(self):
        request = self.factory.get('/account/1/')
        request.user = self.user

        form = AccountCreateForm({'currency': 'USD'})
        self.assertEquals(form.is_valid(), True)

        account = self.account_service.create_account(self.user, form)
        self.assertIsNotNone(account)

        account_detail_view = AccountDetailView()
        response = account_detail_view.get(request, pk=account.account_uuid)

        self.assertEqual(response.status_code, 200)

    def test_account_delete_view(self):
        form = AccountCreateForm({'currency': 'USD'})
        self.assertEquals(form.is_valid(), True)

        account = self.account_service.create_account(self.user, form)
        self.assertIsNotNone(account)

        request = self.factory.post(f'/account/{account.account_uuid}/delete/')
        request.user = self.user

        account_delete_view = AccountDeleteView()
        response = account_delete_view.post(request, pk=account.account_uuid)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)

    def test_account_transfer_view(self):
        form = AccountCreateForm({'currency': 'USD'})
        self.assertEquals(form.is_valid(), True)

        account = self.account_service.create_account(self.user, form)
        self.assertIsNotNone(account)

        request = self.factory.post(f'/account/{account.account_uuid}/transfer/', {'amount': '50'})
        request.user = self.user

        account_transfer_view = AccountTransferView()
        response = account_transfer_view.post(request, pk=account.account_uuid)

        self.assertEqual(response.status_code, 200)  # Redirects to 'account_list'

        # Test scenarios for validation errors, different transactions, and more.

