from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.credit.models import CreditDescription, Credit, PAYMENT_CHOICES
from apps.credit.services.credit_service import CreditDescriptionService, CreditService
from apps.credit.forms import CreditCreateForm


class CreditCreate(View):
    service = CreditService()
    template_form = "credit/credit_create.html"
    model_description = CreditDescription
    model_credit = Credit

    def post(self, request):
        form = CreditCreateForm(request.POST)
        if form.is_valid():
            duration = form.cleaned_data["duration_in_month"]
            rate = form.cleaned_data["rate_index"]
            payment = form.cleaned_data["payment_type"]
            print(f"{duration}, {rate}, {payment}")
            # CreditDescription.objects.create(
            #     duration_in_month=duration,
            #     rate_index=rate,
            #     payment_type=payment)
            print("ok form")

        return render(request, template_name=self.template_form, context={"form": form})

    def get(self, request):
        form = CreditCreateForm()
        return render(request, template_name=self.template_form, context={"form": form})


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
        print(f"---------{durations}-----------")
        return render(request, template_name=self.template_payment, context={"durations": tuple_durations})
