from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

from apps.credit.models import CreditDescription, Credit, PAYMENT_CHOICES
from apps.credit.services.credit_service import CreditDescriptionService, CreditService
from apps.credit.forms import CreditCreateForm
from apps.credit.utils.rate_percent import RatePercent


class CreditCreate(View):
    service_credit = CreditService()
    service_credit_description = CreditDescriptionService()
    template_form = "credit/credit_create.html"
    model_description = CreditDescription
    model_credit = Credit
    rate_percent = RatePercent()

    def post(self, request):
        form = CreditCreateForm(request.POST)
        sum_to_pay = 0.
        if form.is_valid():
            duration = form.cleaned_data["duration_in_month"]
            payment = form.cleaned_data["payment_type"]
            sum_of_credit = form.cleaned_data["sum_of_credit"]
            credit_percent = self.rate_percent.calculate_rate_percent(duration, payment)
            if "take" in request.POST:

                print(f"{duration}, {sum_of_credit}, {payment}, {credit_percent}")
                # CreditDescription.objects.create(
                #     duration_in_month=duration,
                #     rate_index=rate,
                #     payment_type=payment)
            if "calculate" in request.POST:
                sum_to_pay = float(sum_of_credit) + float(sum_of_credit) * credit_percent

        return render(request, template_name=self.template_form,
                      context={"form": form, "sum_to_pay": sum_to_pay})

    def get(self, request):
        form = CreditCreateForm()
        return render(request, template_name=self.template_form,
                      context={"form": form})


class CreditLoadPayment(View):
    template_payment = "credit/credit_payment.html"
    service = CreditDescriptionService()

    def get(self, request):
        duration = request.GET.get("duration_in_month")
        payment_types = self.service.get_with_duration(duration)
        payments = ()
        for i in payment_types:
            if i.payment_type == PAYMENT_CHOICES[0][0]:
                payments += (PAYMENT_CHOICES[0],)
            else:
                payments += (PAYMENT_CHOICES[1],)

        return render(request, template_name=self.template_payment, context={"payment_types": payments})


class CreditLoadDuration(View):
    template_payment = "credit/credit_duration.html"
    service = CreditDescriptionService()

    def get(self, request):
        payment = request.GET.get("payment_type")
        durations_in_month = self.service.get_with_payment(payment)
        durations = []
        for i in durations_in_month:
            durations.append(i.duration_in_month)
        tuple_durations = ()
        for i in set(durations):
            tuple_durations += ((i, i),)
        return render(request, template_name=self.template_payment, context={"durations": tuple_durations})


class RatePercentView(View):
    rate_percent = RatePercent()
    template_payment = "credit/credit_rate.html"

    def get(self, request):
        payment = request.GET.get("payment_type")
        duration = request.GET.get("duration")
        if payment != "" and duration != "":
            rate_percent = self.rate_percent.calculate_rate_percent(duration, payment)
        else:
            rate_percent = 0.0

        return render(request, template_name=self.template_payment, context={"rate_percent": rate_percent})

