from django import forms
from apps.credit.models import Credit, CreditDescription, PAYMENT_CHOICES
from apps.credit.services.credit_service import CreditDescriptionService


class CreditCreateForm(forms.Form):
    descriptions = CreditDescriptionService().get_descriptions()

    durations_list = [i.duration_in_month for i in descriptions]
    durations_list.sort()
    description_duration = tuple((value, value) for value in set(durations_list))
    credit_rate = (CreditDescriptionService()
                   .get_credit_rate(description_duration[0][0], PAYMENT_CHOICES[1][0]).rate_index)

    duration_in_month = forms.ChoiceField(choices=description_duration, initial=description_duration[0])
    payment_type = forms.ChoiceField(choices=PAYMENT_CHOICES, initial=PAYMENT_CHOICES[1])
    sum_of_credit = forms.DecimalField(max_value=999999999.99, max_digits=11, decimal_places=2)
