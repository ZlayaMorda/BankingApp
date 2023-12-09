from django import forms
from apps.credit.models import Credit, CreditDescription, PAYMENT_CHOICES
from apps.credit.services.credit_service import CreditDescriptionService


class CreditCreateForm(forms.Form):
    descriptions = CreditDescriptionService().get_descriptions()

    # descriptions_duration = tuple((list(set([i.duration_in_month for i in descriptions])).index(value), value)
    #                               for value in list(set([i.duration_in_month for i in descriptions])))
    #
    # descriptions_rate = tuple((list(set([i.rate_index for i in descriptions])).index(value), value)
    #                           for value in list(set([i.rate_index for i in descriptions])))
    #
    # descriptions_payment = tuple((list(set([i.payment_type for i in descriptions])).index(value), value)
    #                              for value in list(set([i.payment_type for i in descriptions])))

    description_duration = tuple((value, value)
                                 for value in set([i.duration_in_month for i in descriptions]))
    description_rate = tuple((value, value)
                             for value in set([i.rate_index for i in descriptions]))
    # description_payment = tuple((index, value)
    #                             for index, value in enumerate(set([i.payment_type for i in descriptions])))
    duration_in_month = forms.ChoiceField(
        choices=description_duration)
    rate_index = forms.ChoiceField(
        choices=description_rate)
    payment_type = forms.ChoiceField(
        choices=PAYMENT_CHOICES)
    # credits = forms.ChoiceField(choices=((1, 1), (2, 2)))
