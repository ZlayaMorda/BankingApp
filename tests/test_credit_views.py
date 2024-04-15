import datetime
from audioop import reverse

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from apps.account.models import Account
from apps.credit.views import CreditCreate, CreditLoadPayment, CreditLoadDuration, RatePercentView, CreditList, \
    CreditDetail
from apps.credit.forms import CreditCreateForm  # Import your forms
from apps.credit.models import CreditDescription, Credit  # Import your models as needed
from django.contrib.auth import get_user_model

from utils.exceptions import NotFound


class TestCreditCreateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            first_name='John',
            last_name='Doe',
            password='test123321',
            email='test@gmail.com',
            passport_identifier='1000000A000AA0'
        )

    def test_get_credit_create_view(self):
        request = self.factory.get('/credit/create/')
        request.user = self.user
        response = CreditCreate.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_post_credit_create_view(self):
        request = self.factory.post('/credit/create/', data={
            'duration_in_month': 12,
            'payment_type': 'OM',
            'sum_of_credit': 1000.00,
            'account': 'account_id',
        })
        request.user = self.user
        response = CreditCreate.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestCreditLoadPaymentView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            first_name='John',
            last_name='Doe',
            password='test123321',
            email='test@gmail.com',
            passport_identifier='1000000A000AA0'
        )

    def test_get_credit_load_payment_view(self):
        # Create a sample credit description
        CreditDescription.objects.create(duration_in_month=6, payment_type='OM', rate_index=0.01)
        CreditDescription.objects.create(duration_in_month=12, payment_type='OY', rate_index=0.01)
        # Add more sample CreditDescription objects as needed for testing different scenarios

        request = self.factory.get('/credit/load-payment/')
        request.user = self.user
        request.GET = {'duration_in_month': 6}
        response = CreditLoadPayment.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_credit_load_payment_view_empty(self):
        # Ensure that the view handles empty payment types gracefully
        request = self.factory.get('/credit/load-payment/')
        request.user = self.user
        request.GET = {'duration_in_month': 100}  # Invalid duration
        response = CreditLoadPayment.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestCreditLoadDurationView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            first_name='John',
            last_name='Doe',
            password='test123321',
            email='test@gmail.com',
            passport_identifier='1000000A000AA0'
        )

    def test_get_credit_load_duration_view(self):
        # Create a sample credit description
        CreditDescription.objects.create(duration_in_month=22, payment_type='OM', rate_index=0.01)
        CreditDescription.objects.create(duration_in_month=33, payment_type='OM', rate_index=0.01)
        # Add more sample CreditDescription objects as needed for testing different scenarios

        request = self.factory.get('/credit/load-duration/')
        request.user = self.user
        request.GET = {'payment_type': 'OM'}
        response = CreditLoadDuration.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_get_credit_load_duration_view_empty(self):
        # Ensure that the view handles empty durations gracefully
        request = self.factory.get('/credit/load-duration/')
        request.user = self.user
        request.GET = {'payment_type': 'InvalidPaymentType'}
        response = CreditLoadDuration.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestRatePercentView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            first_name='John',
            last_name='Doe',
            password='test123321',
            email='test@gmail.com',
            passport_identifier='1000000A000AA0'
        )

    def test_get_rate_percent_view(self):
        request = self.factory.get('/rate-percent/')
        request.user = self.user
        request.GET = {'payment_type': 'OM', 'duration': 12}
        response = RatePercentView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestCreditListView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
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
        self.credit = Credit.objects.create(
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

    def test_get_credit_list_view(self):
        request = self.factory.get('/credit/list/')
        request.user = self.user
        response = CreditList.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestCreditDetailView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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
        self.credit = Credit.objects.create(
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

    def test_get_credit_detail_view(self):
        request = self.factory.get('credit_detail', kwargs={'pk': self.credit.pk})
        request.user = self.user
        response = CreditDetail.as_view()(request, pk=self.credit.pk)
        self.assertEqual(response.status_code, 200)

    def test_get_credit_detail_view_no_credit(self):
        request = self.factory.get('credit_detail', kwargs={'pk': 999})  # Non-existing pk
        request.user = self.user
        with self.assertRaises(NotFound):
            CreditDetail.as_view()(request, pk=999)
