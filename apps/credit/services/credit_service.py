import math

from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError

import datetime
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
    "one_off_current_payment": 0.00,
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
        return self.model.objects.filter(payment_type=payment).order_by("duration_in_month")

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
            context["next_payout"] = credit.next_payout.strftime('%m/%d/%Y') if credit.next_payout is not None else "--"
            context["one_off_payment"] = credit.one_off_payment
            context["one_off_current_payment"] = credit.one_off_current_payment
            context["payout_count"] = credit.payout_count
            context["created_at"] = credit.created_at.strftime('%m/%d/%Y')
            context["updated_at"] = credit.created_at.strftime('%m/%d/%Y')
        return context

    def get_credit_context(self, credit, many: bool = False):
        if not credit:
            return None

        if not many:
            context = self.__init_context(credit)
        else:
            context = []
            for cr in credit:
                context.append(self.__init_context(cr))

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
        one_off_current_payment = one_off_payment
        amount_to_pay = one_off_payment * payout_count
        try:
            with transaction.atomic():
                account.amount = float(account.amount) + float(sum_of_credit)
                self.create(amount_to_pay, currency, next_payout, one_off_payment, one_off_current_payment,
                            payout_count, account, description, user)
                account.save()
                return True
        except IntegrityError:
            return False

    def create(self, amount_to_pay, currency, next_payout, one_off_payment, one_off_current_payment, payout_count,
               account, description, user):
        credit = self.model(
            amount_to_pay=amount_to_pay,
            currency=currency,
            next_payout=next_payout,
            one_off_payment=one_off_payment,
            one_off_current_payment=one_off_current_payment,
            payout_count=payout_count,
            account_uuid=account,
            description_uuid=description,
            owner_id=user.user_uuid
        )
        credit.save()

    @staticmethod
    def retrieve_user_credits(user):
        return user.credits.all().order_by("-amount_to_pay")

    def retrieve_credit_pk(self, pk):
        return self.model.objects.filter(pk=pk).first()

    def update_credit_account(self, pk, account):
        credit = self.model.objects.filter(pk=pk).first()
        credit.account_uuid = account
        credit.save()

    def credit_payout(self, credit_pk, sum_to_pay):
        credit = self.retrieve_credit_pk(credit_pk)
        account = credit.account_uuid
        if sum_to_pay <= credit.amount_to_pay and sum_to_pay <= account.amount:
            account.amount -= sum_to_pay

            credit.amount_to_pay -= sum_to_pay
            remember_count = credit.payout_count
            credit.payout_count = math.ceil(credit.amount_to_pay / credit.one_off_payment)
            credit.one_off_current_payment = credit.amount_to_pay % credit.one_off_payment
            diff_count = remember_count - credit.payout_count
            if credit.payout_count == 0:
                try:
                    with transaction.atomic():
                        credit.delete()
                        account.save()
                except IntegrityError:
                    raise IntegrityError()
            else:
                if diff_count != 0:
                    if credit.description_uuid.payment_type == "OM":
                        credit.next_payout += datetime.timedelta(days=30 * diff_count)
                    elif credit.description_uuid.payment_type == "OY":
                        credit.next_payout += datetime.timedelta(days=30 * 12 * diff_count)
                try:
                    with transaction.atomic():
                        account.save()
                        credit.save()
                except IntegrityError:
                    raise IntegrityError()
        else:
            raise ValidationError("Not valid sum of payment")
