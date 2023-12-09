from django import forms
from apps.credit.models import Credit, CreditDescription, PAYMENT_CHOICES
from apps.credit.services.credit_service import CreditDescriptionService


class CreditCreateForm(forms.Form):
    descriptions = CreditDescriptionService().get_descriptions()

    durations_list = [i.duration_in_month for i in descriptions]
    durations_list.sort()
    description_duration = tuple((value, value) for value in set(durations_list))
    description_rate = tuple((value, value)
                             for value in set([i.rate_index for i in descriptions]))

    duration_in_month = forms.ChoiceField(choices=description_duration, initial=description_duration[0])
    payment_type = forms.ChoiceField(choices=PAYMENT_CHOICES, initial=PAYMENT_CHOICES[1])
