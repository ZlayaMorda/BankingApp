from apps.account.models import Account


ACCOUNT_CONTEXT = {
    "owner": {
        "first_name": None,
        "last_name": None,
    },
    "account_uuid": None,
    "currency": None,
    "amount": None,
    "created_at": None,
    "updated_at": None,
}


class AccountService:
    model = Account
    context = ACCOUNT_CONTEXT

    def retrieve_account_by_pk(self, pk) -> Account:
        return self.model.objects.filter(account_uuid=pk).first()

    def get_account_context(self, account: Account) -> ACCOUNT_CONTEXT:
        context = ACCOUNT_CONTEXT
        context["owner"]["first_name"] = account.owner.first_name
        context["owner"]["last_name"] = account.owner.last_name
        context["id"] = account.account_uuid
        context["currency"] = account.currency
        context["amount"]: account.amount
        context["created_at"]: account.created_at
        context["updated_at"]: account.updated_at

        return context
