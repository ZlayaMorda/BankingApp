import unittest
from unittest.mock import MagicMock, patch
from django.utils import timezone
from apps.account.services.account_service import AccountService

class TestAccountService(unittest.TestCase):
    def setUp(self):
        self.account_service = AccountService()

    def test_init_context_with_account(self):
        account = MagicMock(owner=MagicMock(first_name='John', last_name='Doe'),
                            account_uuid='123456', currency='USD', amount=100.00,
                            created_at=timezone.now())

        context = self.account_service._AccountService__init_context(account)

        self.assertEqual(context['owner']['first_name'], 'John')
        self.assertEqual(context['owner']['last_name'], 'Doe')
        self.assertEqual(context['id'], '123456')
        self.assertEqual(context['currency'], 'USD')
        self.assertEqual(context['amount'], 100.00)
        self.assertIsNotNone(context['created_at'])
        self.assertIsNotNone(context['updated_at'])

    @patch('apps.account.models.Account.objects')
    def test_retrieve_account_by_pk(self, mock_account_objects):
        # Create a MagicMock for the returned value of 'first()'
        mock_first = MagicMock()
        mock_first.account_uuid = '123456'

        # Create a MagicMock for the 'filter()' method
        mock_filter = MagicMock()
        mock_filter.first.return_value = mock_first

        # Set up the behavior of 'objects.filter(account_uuid=pk).first()'
        mock_account_objects.filter.return_value = mock_filter

        # Call the method being tested
        account = self.account_service.retrieve_account_by_pk('123456')

        # Assertions
        self.assertIsNotNone(account)
        self.assertEqual(account.account_uuid, '123456')

    def test_retrieve_user_accounts(self):
        user_mock = MagicMock(accounts=MagicMock(all=MagicMock(return_value=[MagicMock(), MagicMock()])))

        accounts = self.account_service.retrieve_user_accounts(user_mock)
        self.assertEqual(len(accounts), 2)

        user_mock.accounts.all = MagicMock(return_value=[])
        accounts = self.account_service.retrieve_user_accounts(user_mock)
        self.assertEqual(len(accounts), 0)

    @patch('apps.account.services.third_party_api.ExchangeRateAPI.calculate_amount')
    @patch('apps.account.models.Account.objects.get')
    def test_execute_account_transaction(self, mock_get, mock_calculate_amount):
        # Mock source and destination accounts
        source_account = MagicMock(account_uuid='source_uuid', currency='USD', amount=100.00)
        destination_account = MagicMock(account_uuid='destination_uuid', currency='EUR', amount=200.00)

        # Set side effects for mock objects
        mock_get.side_effect = [source_account, destination_account]
        mock_calculate_amount.return_value = 50.00

        # Call the method being tested
        self.account_service.execute_account_transaction('source_uuid', 'destination_uuid', 30.00)

        # Assertions
        self.assertEqual(source_account.amount, 70.00)  # Check if the amount was deducted correctly
        self.assertEqual(destination_account.amount, 250.00)  # Check if the amount was added correctly
