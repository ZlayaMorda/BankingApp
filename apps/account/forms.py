from django import forms
from apps.account.models import Account
from apps.account.services.account_service import AccountService

class AccountCreateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['currency']


class AccountTransferForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        service = AccountService()
        accounts = service.retrieve_user_accounts(user)
        accounts_tuple = tuple((acc.account_uuid, acc.account_uuid) for acc in accounts)
        accounts_tuple += (("--", "--"),)
        self.fields['amount'] = forms.DecimalField(required=True)
        self.fields['own_accounts'] = forms.ChoiceField(
            choices=accounts_tuple,
            initial="--"
        )
        self.fields['destination_account'] = forms.UUIDField(required=False)
