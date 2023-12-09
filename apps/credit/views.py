from django.shortcuts import render, redirect
from django.views import View
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from apps.account.services.account_service import AccountService
from apps.credit.models import CreditDescription, Credit, PAYMENT_CHOICES
from apps.credit.services.credit_service import CreditDescriptionService, CreditService
from apps.credit.forms import CreditCreateForm, CreditChangeAccount, CreditPayment
from apps.credit.utils.rate_percent import RatePercent
from utils.exceptions import AuthException, NotFound
from utils.permissions import logged_in


class CreditCreate(View):
    service_credit = CreditService()
    service_credit_description = CreditDescriptionService()
    template_form = "credit/credit_create.html"
    rate_percent = RatePercent()

    @logged_in
    def post(self, request):
        form = CreditCreateForm(request.user, request.POST)
        sum_to_pay = 0.
        credit_percent = 0.
        if form.is_valid():
            duration = form.cleaned_data["duration_in_month"]
            payment = form.cleaned_data["payment_type"]
            sum_of_credit = form.cleaned_data["sum_of_credit"]
            account = form.cleaned_data["account"]
            credit_percent = self.rate_percent.calculate_rate_percent(duration, payment)
            if "take" in request.POST and account != "":
                self.service_credit.calculate_and_create(request.user, int(duration), payment,
                                                         float(sum_of_credit), account, credit_percent)
                return redirect("credit_list")
            if "calculate" in request.POST:
                sum_to_pay = round(float(sum_of_credit) + float(sum_of_credit) * credit_percent, 2)

        return render(request, template_name=self.template_form,
                      context={"form": form, "sum_to_pay": sum_to_pay, "rate_percent": credit_percent})

    @logged_in
    def get(self, request):
        form = CreditCreateForm(request.user)
        return render(request, template_name=self.template_form,
                      context={"form": form, "rate_percent": form.rate_percent})


class CreditLoadPayment(View):
    template_payment = "credit/credit_payment.html"
    service = CreditDescriptionService()

    @logged_in
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

    @logged_in
    def get(self, request):
        payment = request.GET.get("payment_type")
        durations_in_month = self.service.get_with_payment(payment)
        durations = []
        for i in durations_in_month:
            durations.append(i.duration_in_month)
        tuple_durations = ()
        for i in durations:
            tuple_durations += ((i, i),)
        return render(request, template_name=self.template_payment, context={"durations": tuple_durations})


class RatePercentView(View):
    rate_percent = RatePercent()
    template_payment = "credit/credit_rate.html"

    @logged_in
    def get(self, request):
        payment = request.GET.get("payment_type")
        duration = request.GET.get("duration")
        if payment != "" and duration != "":
            rate_percent = self.rate_percent.calculate_rate_percent(duration, payment)
        else:
            rate_percent = 0.0

        return render(request, template_name=self.template_payment, context={"rate_percent": rate_percent})


class CreditList(View):
    service = CreditService()
    template = "credit/credit_list.html"

    @logged_in
    def get(self, request):
        context = {}
        user_credits = self.service.retrieve_user_credits(request.user)
        context["credits"] = self.service.get_credit_context(user_credits, True)

        return render(request, template_name=self.template, context=context)


class CreditDetail(View):
    service_credit = CreditService()
    service_account = AccountService()
    template = "credit/credit_detail.html"

    @logged_in
    def get(self, request, pk):
        form_account = CreditChangeAccount(request.user)
        form_payment = CreditPayment()
        context = {"form_account": form_account, "form_payment": form_payment}
        credit = self.service_credit.retrieve_credit_pk(pk)
        if not credit:
            raise NotFound("Credit does not exist")
        if credit.owner_id == request.user.user_uuid:
            context["credit"] = self.service_credit.get_credit_context(credit)
            return render(request, template_name=self.template, context=context)
        else:
            raise AuthException()

    @logged_in
    def post(self, request, pk):
        form_account_post = CreditChangeAccount(request.user, request.POST)
        form_payment_post = CreditPayment(request.POST)
        form_account = CreditChangeAccount(request.user)
        form_payment = CreditPayment()

        credit = self.service_credit.retrieve_credit_pk(pk)
        if not credit:
            raise NotFound("Credit does not exist")

        if credit.owner_id == request.user.user_uuid:
            validation_state = ""
            if "change_button" in request.POST:
                form_account = form_account_post
                if form_account_post.is_valid():
                    account_form = form_account_post.cleaned_data["account"]
                    account = self.service_account.retrieve_account_by_pk(account_form)
                    if account.owner_id == request.user.user_uuid:
                        if credit.currency == account.currency:
                            self.service_credit.update_credit_account(pk, account)
                        else:
                            validation_state = "Currency must be the same"
                    else:
                        raise AuthException()
            elif "payment_button" in request.POST:
                form_payment = form_payment_post
                if form_payment_post.is_valid():
                    sum_to_pay = form_payment_post.cleaned_data["payment"]
                    try:
                        self.service_credit.credit_payout(pk, sum_to_pay)
                    except IntegrityError:
                        validation_state = "Payment Error, try again"
                    except ValidationError as e:
                        validation_state = e.message

            context = {"form_account": form_account, "form_payment": form_payment,
                       "validation_state": validation_state}
            credit = self.service_credit.retrieve_credit_pk(pk)
            if not credit:
                return redirect("credit_list")
            context["credit"] = self.service_credit.get_credit_context(credit)
            return render(request, template_name=self.template, context=context)
        else:
            raise AuthException()
