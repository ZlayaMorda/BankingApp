from django.shortcuts import render
from django.views import View
from apps.account.services.account_service import AccountService


class AccountDetailView(View):
    template_name = "account.html"
    service = AccountService()

    def get(self, request, pk):
        context = {}
        account = self.service.retrieve_account_by_pk(pk=pk)
        if account:
            context['account'] = self.service.get_account_context(account)
        return render(request, template_name=self.template_name, context=context)
