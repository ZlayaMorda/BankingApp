from django.shortcuts import render, redirect
from django.views import View
from apps.account.services.account_service import AccountService
from django.contrib.auth.models import AnonymousUser
from apps.account.forms import AccountCreateForm, AccountTransferForm

class AccountDetailView(View):
    template_name = "account/account_detail.html"
    service = AccountService()
    account_transfer_form = AccountTransferForm

    def get(self, request, pk):
        context = {
            'account_transfer_form': self.account_transfer_form(request.user)
        }
        account = self.service.retrieve_account_by_pk(pk=pk)
        if account:
            context['account'] = self.service.get_account_context(account)
        return render(request, template_name=self.template_name, context=context)


class AccountListView(View):
    template_name = "account/account_list.html"
    service = AccountService()
    account_create_form = AccountCreateForm

    def get(self, request):
        context = {"account_create_form": self.account_create_form}

        if request.user is not AnonymousUser:
            user = request.user
            accounts = self.service.retrieve_user_accounts(user=user)
            context['accounts'] = self.service.get_account_context(accounts, many=True)
        else:
            context = {'message': 'Not Authorized'}
            return render(request, template_name='error/error.html', context=context)

        return render(request, template_name='account/account_list.html', context=context)


class AccountCreateView(View):
    service = AccountService()

    def post(self, request):
        form = AccountCreateForm(request.POST)
        if form.is_valid():
            self.service.create_account(request.user, form)
        return redirect('account_list')


class AccountDeleteView(View):
    service = AccountService()

    def delete(self, request, pk):
        self.service.delete_account(pk)
        return redirect('account_list')


class AccountTransferVuew(View):
    service = AccountService()

    def post(self, request):

        return redirect('account_list')
