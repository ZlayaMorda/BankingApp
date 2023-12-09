from django import forms

from apps.account.models import CURRENCY_CHOICES, Account


class AccountCreateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['currency']