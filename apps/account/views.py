from django.shortcuts import render
from django.views import View
from apps.account.services.account_service import AccountService
from django.contrib.auth.models import AnonymousUser

class AccountDetailView(View):
    template_name = "account/account_detail.html"
    service = AccountService()

    def get(self, request, pk):
        context = {}
        account = self.service.retrieve_account_by_pk(pk=pk)
        if account:
            context['account'] = self.service.get_account_context(account)
        return render(request, template_name=self.template_name, context=context)


class AccountListCreateView(View):
    template_name = "account/account_list.html"
    service = AccountService()

    def get(self, request):
        context = {}

        if request.user is not AnonymousUser:
            user = request.user
            accounts = self.service.retrieve_user_accounts(user=user)
            context['accounts'] = self.service.get_account_context(accounts, many=True)
        else:
            context = {'message': 'Not Authorized'}
            return render(request, template_name='error/error.html', context=context)

        return render(request, template_name='account/account_list.html', context=context)


    def post(self, request):
        pass