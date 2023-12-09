from apps.account.models import Account
from django.db import transaction

from apps.credit.models import Credit

ACCOUNT_CONTEXT = {
    "owner": {
        "first_name": None,
        "last_name": None,
    },
    "account_uuid": None,
    "currency": None,
    "amount": 0.00,
    "created_at": None,
    "updated_at": None,
}


class AccountService:
    model = Account

    def __init_context(self, account):
        context = ACCOUNT_CONTEXT.copy()
        if account:
            context["owner"]["first_name"] = account.owner.first_name
            context["owner"]["last_name"] = account.owner.last_name
            context["id"] = account.account_uuid
            context["currency"] = account.currency
            context["amount"] = account.amount
            context["created_at"] = (account.created_at).strftime('%m/%d/%Y')
            context["updated_at"] = (account.created_at).strftime('%m/%d/%Y')
        return context

    def retrieve_account_by_pk(self, pk) -> Account:
        return self.model.objects.filter(account_uuid=pk).first()

    def retrieve_user_accounts(self, user) -> [Account]:
        return user.accounts.all()

    def get_account_context(self, account, many: bool = False):
        context = ACCOUNT_CONTEXT
        if not account:
            return None

        if not many:
            context = self.__init_context(account)
        else:
            context = []
            for acc in account:
                context.append(self.__init_context(acc))

        return context

    def create_account(self, user, form):
        currency = form.cleaned_data['currency']
        Account.objects.create(owner=user, currency=currency)
        return True

    def delete_account(self, pk):
        credit = Credit.objects.filter(account_uuid_id=pk).first()
        account = Account.objects.filter(account_uuid=pk).first()
        if credit or account.amount > 0:
            return None
        result = account.delete()
        return result

    def execute_account_transaction(self, source_account_uuid, destination_account_uuid, amount):
        with transaction.atomic():
            if source_account_uuid == destination_account_uuid:
                raise ValueError('Using the same source and destination accounts is not allowed.')

            source_account = Account.objects.get(account_uuid=source_account_uuid)
            destination_account = Account.objects.get(account_uuid=destination_account_uuid)

            if source_account.amount - amount < 0:
                raise ValueError('Insufficient funds')

            source_account.amount -= amount
            destination_account.amount += amount

            source_account.save()
            destination_account.save()
