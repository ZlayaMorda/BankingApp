from apps.account.models import Account
from django.db import transaction
from web3 import Web3
import json

from apps.account.services.third_party_api import ExchangeRateAPI
from apps.credit.models import Credit
from banking.settings import BC_URL, CONTRACT_ADDRESS, PRIVATE_KEY
from utils.exceptions import CustomValueError

ACCOUNT_CONTEXT = {
    "owner": {
        "first_name": None,
        "last_name": None,
    },
    "account_uuid": None,
    "currency": None,
    "amount": 0.00,
    "created_at": None,
    "updated_at": None,
}


class AccountService:
    model = Account

    def __init_context(self, account):
        context = ACCOUNT_CONTEXT.copy()
        if account:
            context["owner"]["first_name"] = account.owner.first_name
            context["owner"]["last_name"] = account.owner.last_name
            context["id"] = account.account_uuid
            context["currency"] = account.currency
            context["amount"] = account.amount
            context["created_at"] = (account.created_at).strftime('%m/%d/%Y')
            context["updated_at"] = (account.created_at).strftime('%m/%d/%Y')
        return context

    def retrieve_account_by_pk(self, pk) -> Account:
        return self.model.objects.filter(account_uuid=pk).first()

    def retrieve_user_accounts(self, user) -> [Account]:
        return user.accounts.all()

    def get_account_context(self, account, many: bool = False):
        context = ACCOUNT_CONTEXT
        if not account:
            return None

        if not many:
            context = self.__init_context(account)
        else:
            context = []
            for acc in account:
                context.append(self.__init_context(acc))

        return context

    def create_account(self, user, form):
        currency = form.cleaned_data['currency']
        return Account.objects.create(owner=user, currency=currency)

    def delete_account(self, pk):
        credit = Credit.objects.filter(account_uuid_id=pk).first()
        account = Account.objects.filter(account_uuid=pk).first()
        if credit or account.amount > 0:
            return None
        result = account.delete()
        return result

    def execute_account_transaction(self, source_account_uuid, destination_account_uuid, amount):
        with transaction.atomic():
            if source_account_uuid == destination_account_uuid:
                raise CustomValueError('Using the same source and destination accounts is not allowed.')

            source_account = Account.objects.get(account_uuid=source_account_uuid)
            destination_account = Account.objects.get(account_uuid=destination_account_uuid)

            if source_account.amount - amount < 0:
                raise CustomValueError('Insufficient funds')

            amount_to_send = ExchangeRateAPI().calculate_amount(source_account.currency,
                                                                destination_account.currency, amount)
            source_account.amount -= amount
            destination_account.amount += amount_to_send

            source_account.save()
            destination_account.save()

    def exchange_for_token(self, account, amount, bc_account):
        amount_to_get = ExchangeRateAPI().calculate_amount(account.currency, "BYN", amount)
        if account.amount - amount < 0:
            raise ValueError('Insufficient funds')
        account.amount -= amount
        account.save()

        w3 = Web3(Web3.HTTPProvider(BC_URL))
        if not w3.is_connected():
            raise ConnectionError("Failed to connect to HTTPProvider")

        with open("web3/artifacts/contracts/BYNToken.sol/BYNToken.json") as abi_file:
            contract_abi = json.load(abi_file)["abi"]

        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)
        token_amount = w3.to_wei(amount_to_get, 'ether')
        nonce = w3.eth.get_transaction_count(w3.eth.account.from_key(PRIVATE_KEY).address)

        # transaction = contract.functions.transfer(bc_account, token_amount).transact({
        #     'chainId': w3.eth.chain_id,
        #     'gas': 200000,  # Adjust the gas limit as needed
        #     'nonce': nonce,
        # })
        transaction = contract.functions.transfer(bc_account, token_amount).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 200000,  # Adjust the gas limit as needed
            'nonce': nonce,
        })
        signed_txn = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

        try:
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Transaction sent! Hash: {tx_hash.hex()}")
        except Exception as e:
            account.amount += amount
            account.save()
            raise e
