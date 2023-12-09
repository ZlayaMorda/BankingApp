from django import forms
from apps.credit.models import Credit, CreditDescription, PAYMENT_CHOICES
from apps.credit.services.credit_service import CreditDescriptionService
from apps.credit.utils.rate_percent import RatePercent


class CreditCreateForm(forms.Form):
    descriptions = CreditDescriptionService().get_descriptions()

    durations_list = [i.duration_in_month for i in descriptions]
    durations_list.sort()
    description_duration = tuple((value, value) for value in set(durations_list))
    rate_percent = RatePercent().calculate_rate_percent(description_duration[0][0], PAYMENT_CHOICES[1][0])

    duration_in_month = forms.ChoiceField(choices=description_duration, initial=description_duration[0])
    payment_type = forms.ChoiceField(choices=PAYMENT_CHOICES, initial=PAYMENT_CHOICES[1])
    sum_of_credit = forms.DecimalField(max_value=999999999.99, min_value=100.0, max_digits=11, decimal_places=2)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        accounts = user.accounts.all()
        accounts_list = [i.account_uuid for i in accounts]
        accounts_tuple = tuple((value, value) for value in accounts_list)
        self.account = forms.ChoiceField(choices=accounts_tuple, required=False)
        super().__init__(*args, **kwargs)
