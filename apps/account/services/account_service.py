import uuid
from datetime import datetime
from apps.account.models import Account
from apps.account.models import CURRENCY_CHOICES

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
            context["amount"]: account.amount
            a = account.created_at
            context["created_at"] = (account.created_at).strftime('%m/%d/%Y')
            context["updated_at"] = (account.created_at).strftime('%m/%d/%Y')
        return context

    def retrieve_account_by_pk(self, pk) -> Account:
        return self.model.objects.filter(account_uuid=pk).first()

    def retrieve_user_accounts(self, user) -> [Account]:
        a = bool(user.accounts)
        return user.accounts.all()

    def get_account_context(self, account, many: bool = False):
        context = ACCOUNT_CONTEXT
        if not account:
            return ACCOUNT_CONTEXT

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
