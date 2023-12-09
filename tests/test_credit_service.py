import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from apps.credit.models import Credit, CreditDescription
from apps.account.models import Account
from apps.credit.services.credit_service import CreditDescriptionService, CreditService


class CreditDescriptionServiceTest(TestCase):
    def setUp(self):
        self.description = CreditDescription.objects.create(
            duration_in_month=345,
            payment_type="OM",
            rate_index=0.05
        )

    def test_get_descriptions(self):
        descriptions = CreditDescriptionService().get_descriptions().filter(rate_index=0.05)
        self.assertEqual(len(descriptions), 1)

    def test_get_description_by_duration_and_payment(self):
        description = CreditDescriptionService().get_description_by_duration_and_payment(345, "OM")
        self.assertEqual(description, self.description)


class CreditServiceTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name='John',
            last_name='Doe',
            password='test123321',
            email='test@gmail.com',
            passport_identifier='1000000A000AA0'
        )
        self.account = Account.objects.create(owner=self.user, currency="USD", amount=1000)
        self.credit_description = CreditDescription.objects.create(
            duration_in_month=50,
            payment_type="OM",
            rate_index=0.05
        )

    def test_calculate_and_create_credit(self):
        sum_of_credit = 500
        credit_percent = 0.1
        duration = 50
        payment = "OM"
        credit_service = CreditService()

        # Test create credit
        result = credit_service.calculate_and_create(self.user, duration, payment, sum_of_credit,
                                                     self.account.pk, credit_percent)
        self.assertTrue(result)

    def test_credit_payout(self):
        # Create a credit
        credit = Credit.objects.create(
            amount_to_pay=500,
            currency="USD",
            next_payout=datetime.datetime.now(),
            one_off_payment=50,
            one_off_current_payment=50,
            payout_count=10,
            account_uuid=self.account,
            description_uuid=self.credit_description,
            owner_id=self.user.user_uuid
        )

        # Test successful credit payout
        sum_to_pay = 200
        credit_service = CreditService()
        credit_service.credit_payout(credit.pk, sum_to_pay)
        updated_credit = Credit.objects.get(pk=credit.pk)
        self.assertEqual(updated_credit.amount_to_pay, 300)

    def test_credit_payout_complete_payment_and_credit_deletion(self):
        # Create a credit
        credit = Credit.objects.create(
            amount_to_pay=100,
            currency="USD",
            next_payout=datetime.datetime.now(),
            one_off_payment=10,
            one_off_current_payment=10,
            payout_count=10,
            account_uuid=self.account,
            description_uuid=self.credit_description,
            owner_id=self.user.user_uuid
        )

        # Test complete credit payment and deletion
        sum_to_pay = 100
        credit_service = CreditService()
        credit_service.credit_payout(credit.pk, sum_to_pay)

        # Check if the credit was deleted
        with self.assertRaises(Credit.DoesNotExist):
            Credit.objects.get(pk=credit.pk)

    def test_credit_payout_insufficient_account_balance(self):
        # Create a credit
        credit = Credit.objects.create(
            amount_to_pay=500,
            currency="USD",
            next_payout=datetime.datetime.now(),
            one_off_payment=50,
            one_off_current_payment=50,
            payout_count=10,
            account_uuid=self.account,
            description_uuid=self.credit_description,
            owner_id=self.user.user_uuid
        )

        # Test payout with an amount greater than the account balance
        sum_to_pay = 1000
        credit_service = CreditService()

        with self.assertRaises(ValidationError):
            credit_service.credit_payout(credit.pk, sum_to_pay)

    def test_credit_payout_insufficient_credit_amount(self):
        # Create a credit
        credit = Credit.objects.create(
            amount_to_pay=500,
            currency="USD",
            next_payout=datetime.datetime.now(),
            one_off_payment=50,
            one_off_current_payment=50,
            payout_count=10,
            account_uuid=self.account,
            description_uuid=self.credit_description,
            owner_id=self.user.user_uuid
        )

        # Test payout with an amount greater than remaining credit amount
        sum_to_pay = 600
        credit_service = CreditService()

        with self.assertRaises(ValidationError):
            credit_service.credit_payout(credit.pk, sum_to_pay)
