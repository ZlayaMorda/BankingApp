import datetime
import uuid

from apps.account.services.account_service import AccountService
from apps.credit.models import Credit, CreditDescription
from utils.exceptions import NotFound


class CreditDescriptionService:
    model = CreditDescription

    def get_descriptions(self):
        return self.model.objects.all()

    def get_description_by_duration_and_payment(self, duration, payment):
        return self.model.objects.filter(duration_in_month=duration, payment_type=payment).first()

    def get_with_duration(self, duration):
        return self.model.objects.filter(duration_in_month=duration)

    def get_with_payment(self, payment):
        return self.model.objects.filter(payment_type=payment)

    def get_credit_rate(self, duration, payment):
        try:
            return float(self.model.objects.filter(duration_in_month=duration, payment_type=payment).first().rate_index)
        except Exception:
            raise NotFound("Not valid credit description")


class CreditService:
    model = Credit

    def get_descriptions(self):
        return self.model.objects.all()

    def calculate_and_create(self, user, duration, payment, sum_of_credit, account, credit_percent):
        account = AccountService().retrieve_account_by_pk(account)
        currency = account.currency
        payout_count = 0
        next_payout = datetime.datetime.now()
        description = CreditDescriptionService().get_description_by_duration_and_payment(duration, payment)

        if payment == "OM":
            payout_count = duration
            next_payout += datetime.timedelta(days=30)
        elif payment == "OY":
            payout_count = duration / 12
            next_payout += datetime.timedelta(days=30*12)

        one_off_payment = round((float(sum_of_credit) + float(sum_of_credit) * credit_percent) / payout_count, 2)
        amount_to_pay = one_off_payment * payout_count
        self.create(amount_to_pay, currency, next_payout, one_off_payment, payout_count,
                    account, description, user)

    def create(self, amount_to_pay, currency, next_payout, one_off_payment, payout_count,
               account, description, user):
        credit = self.model(
            amount_to_pay=amount_to_pay,
            currency=currency,
            next_payout=next_payout,
            one_off_payment=one_off_payment,
            payout_count=payout_count,
            account_uuid=account,
            description_uuid=description,
            owner_id=user
        )
        credit.save()
