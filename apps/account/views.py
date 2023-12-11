import decimal
import json
from web3 import Web3
from django.shortcuts import render, redirect
from django.views import View
from apps.account.services.account_service import AccountService
from apps.account.forms import AccountCreateForm, AccountTransferForm
from utils.exceptions import AuthException, NotFound
from apps.account.services.validators import validate_decimal_value
from utils.permissions import logged_in
from utils.exceptions import CustomValueError
from django.http import JsonResponse
from urllib.parse import parse_qs
from banking.settings import CONTRACT_ADDRESS


class AccountDetailView(View):
    template_name = "account/account_detail.html"
    service = AccountService()
    account_transfer_form = AccountTransferForm

    @logged_in
    def get(self, request, pk):
        context = {
            'account_transfer_form': self.account_transfer_form(request.user),
            "tokenAddress": CONTRACT_ADDRESS,
        }
        account = self.service.retrieve_account_by_pk(pk=pk)
        if not account:
            raise NotFound("Account does not exist")
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
    def post(self, request, pk):
        account = self.service.retrieve_account_by_pk(pk=pk)
        if not account:
            raise NotFound("Account does not exist")
        if account.owner == request.user:
            if self.service.delete_account(pk):
                return JsonResponse({'status': '200'})
            else:
                return redirect("account_detail", pk)
        else:
            raise AuthException()


class AccountTransferView(View):
    service = AccountService()

    def get_account(self, request, pk, context):
        account = self.service.retrieve_account_by_pk(pk=pk)
        if not account:
            raise NotFound("Account does not exist")
        if account.owner != request.user:
            raise AuthException()
        context["account"] = self.service.get_account_context(account)

    @logged_in
    def post(self, request, pk):
        form = AccountTransferForm(request.user, request.POST)
        context = {"account_transfer_form": form, "tokenAddress": CONTRACT_ADDRESS,}

        if request.POST.get("destination_account", None) and request.POST.get("own_accounts", None) != '--':
            form.add_error("destination_account", "Only one destination field must be chosen")
            self.get_account(request, pk, context)
            return render(request, template_name="account/account_detail.html", context=context)

        if not request.POST.get("destination_account", None) and request.POST.get("own_accounts", None) == '--':
            form.add_error("destination_account", "Destination must be chosen")
            self.get_account(request, pk, context)
            return render(request, template_name="account/account_detail.html", context=context)

        if form.is_valid():
            amount = form.cleaned_data["amount"]
            amount = decimal.Decimal(amount)
            destination = form.cleaned_data["destination_account"]
            source = pk
            own_account = form.cleaned_data["own_accounts"]
            account = self.service.retrieve_account_by_pk(pk=pk)
            if not account:
                raise NotFound("Account does not exist")
            if account.owner != request.user:
                raise AuthException()
            try:
                if own_account != "--":
                    self.service.execute_account_transaction(str(source), str(own_account), amount)
                elif destination is not None:
                    self.service.execute_account_transaction(str(source), str(destination), amount)
                else:
                    account = self.service.retrieve_account_by_pk(pk=pk)
                    context["account"] = self.service.get_account_context(account)
                    return render(request, template_name="account/account_detail.html", context=context)
            except CustomValueError as e:
                form.add_error("destination_account", e.message)
                self.get_account(request, pk, context)
                return render(request, template_name="account/account_detail.html", context=context)

        else:
            self.get_account(request, pk, context)
            return render(request, template_name="account/account_detail.html", context=context)

        return redirect("account_list")


class AccountTokenView(View):
    service = AccountService()

    def get_account(self, request, pk, context):
        account = self.service.retrieve_account_by_pk(pk=pk)
        if not account:
            raise NotFound("Account does not exist")
        if account.owner != request.user:
            raise AuthException()
        context["account"] = self.service.get_account_context(account)

    @logged_in
    def post(self, request, pk):
        parsed_data = parse_qs(request.body.decode("utf-8"))
        data = {key: value[0] if len(value) == 1 else value for key, value in parsed_data.items()}
        context = {"account_transfer_form": AccountTransferForm(request.user), "tokenAddress": CONTRACT_ADDRESS}
        try:
            data["amount"] = decimal.Decimal(data["amount"])
        except KeyError:
            context["token"] = True
            context["content"] = "Invalid amount"
            self.get_account(request, pk, context)
            return render(request, template_name="account/account_detail.html", context=context)

        if validate_decimal_value(data["amount"]):
            try:
                if len(data["bc_account"]) == 42:
                    amount = data["amount"]
                    bc_account = Web3.to_checksum_address(data["bc_account"])
                    account = self.service.retrieve_account_by_pk(pk=pk)
                    if not account:
                        raise NotFound("Account does not exist")
                    if account.owner != request.user:
                        raise AuthException()
                    else:
                        self.service.exchange_for_token(account, amount, bc_account)
                        context["account"] = self.service.get_account_context(account)

                        return render(request, template_name="account/account_detail.html", context=context)
                else:
                    self.get_account(request, pk, context)
                    context["token"] = True
                    context["content"] = "Invalid blockchain account"
                    return render(request, template_name="account/account_detail.html", context=context)
            except KeyError:
                self.get_account(request, pk, context)
                context["token"] = True
                context["content"] = "Invalid blockchain account"
            except ValueError:
                self.get_account(request, pk, context)
                context["content"] = "Insufficient funds, check account amount"
                context["token"] = True
            except ConnectionError:
                self.get_account(request, pk, context)
                context["content"] = "Problem connecting to network, try again later"
                context["token"] = True
            finally:
                return render(request, template_name="account/account_detail.html", context=context)
        else:
            self.get_account(request, pk, context)
            context["token"] = True
            context["content"] = "Invalid amount"
            return render(request, template_name="account/account_detail.html", context=context)


