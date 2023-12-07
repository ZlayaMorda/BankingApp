import decimal
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from apps.account.services.account_service import AccountService
from django.contrib.auth.models import AnonymousUser
from apps.account.forms import AccountCreateForm, AccountTransferForm
from utils.exceptions import AuthException
from utils.permissions import logged_in


class AccountDetailView(View):
    template_name = "account/account_detail.html"
    service = AccountService()
    account_transfer_form = AccountTransferForm

    @logged_in
    def get(self, request, pk):
        context = {
            'account_transfer_form': self.account_transfer_form(request.user)
        }
        account = self.service.retrieve_account_by_pk(pk=pk)
        if account.owner == request.user:
            if account:
                context['account'] = self.service.get_account_context(account)
            return render(request, template_name=self.template_name, context=context)
        else:
            raise AuthException()


class AccountListView(View):
    template_name = "account/account_list.html"
    service = AccountService()
    account_create_form = AccountCreateForm

    @logged_in
    def get(self, request):
        context = {"account_create_form": self.account_create_form}

        user = request.user
        accounts = self.service.retrieve_user_accounts(user=user)
        context['accounts'] = self.service.get_account_context(accounts, many=True)

        return render(request, template_name='account/account_list.html', context=context)


class AccountCreateView(View):
    service = AccountService()

    @logged_in
    def post(self, request):
        form = AccountCreateForm(request.POST)
        if form.is_valid():
            self.service.create_account(request.user, form)
        return redirect('account_list')


class AccountDeleteView(View):
    service = AccountService()

    @logged_in
    def delete(self, request, pk):
        account = self.service.retrieve_account_by_pk(pk=pk)
        if account.owner == request.user:
            if self.service.delete_account(pk):
                return redirect("account_list")
            else:
                return redirect("account_detail", pk)
        else:
            raise AuthException()


class AccountTransferView(View):
    service = AccountService()

    @logged_in
    def post(self, request, pk):
        form = AccountTransferForm(request.user, request.POST)
        context = {"account_transfer_form": form}
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            amount = decimal.Decimal(amount)
            destination = form.cleaned_data["destination_account"]
            source = pk
            own_account = form.cleaned_data["own_accounts"]
            if own_account != "--":
                account = self.service.retrieve_account_by_pk(pk=pk)
                if account.owner == request.user:
                    self.service.execute_account_transaction(str(source), str(own_account), amount)
                else:
                    raise AuthException()
            elif destination is not None:
                self.service.execute_account_transaction(str(source), str(destination), amount)
            else:
                account = self.service.retrieve_account_by_pk(pk=pk)
                context["account"] = self.service.get_account_context(account)
                return render(request, template_name="account/account_detail.html", context=context)
        else:
            account = self.service.retrieve_account_by_pk(pk=pk)
            context["account"] = self.service.get_account_context(account)
            return render(request, template_name="account/account_detail.html", context=context)

        return redirect("account_list")
