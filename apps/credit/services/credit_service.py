import datetime
import uuid

from apps.account.services.account_service import AccountService
from apps.credit.models import Credit, CreditDescription
from utils.exceptions import NotFound

CREDIT_CONTEXT = {
    "owner": {
        "first_name": None,
        "last_name": None,
    },
    "account": None,
    "credit_uuid": None,
    "currency": None,
    "amount_to_pay": 0.00,
    "next_payout": None,
    "one_off_payment": 0.00,
    "payout_count": 0,
    "created_at": None,
    "updated_at": None,
}


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

    @staticmethod
    def __init_context(credit):
        context = CREDIT_CONTEXT.copy()
        if credit:
            context["owner"]["first_name"] = credit.owner.first_name
            context["owner"]["last_name"] = credit.owner.last_name
            context["account"] = credit.account_uuid_id
            context["credit_uuid"] = credit.credit_uuid
            context["currency"] = credit.currency
            context["amount_to_pay"] = credit.amount_to_pay
            context["next_payout"] = credit.next_payout.strftime('%m/%d/%Y')
            context["one_off_payment"] = credit.one_off_payment
            context["payout_count"] = credit.payout_count
            context["created_at"] = credit.created_at.strftime('%m/%d/%Y')
            context["updated_at"] = credit.created_at.strftime('%m/%d/%Y')
        return context

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
            next_payout += datetime.timedelta(days=30 * 12)

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
            owner_id=user.user_uuid
        )
        credit.save()

    @staticmethod
    def retrieve_user_credits(user):
        return user.credits.all()

    def get_credit_context(self, credit, many: bool = False):
        if not credit:
            return CREDIT_CONTEXT

        if not many:
            context = self.__init_context(credit)
        else:
            context = []
            for cr in credit:
                context.append(self.__init_context(cr))

        return context

    def retrieve_credit_pk(self, pk):
        return self.model.objects.filter(pk=pk).first()
