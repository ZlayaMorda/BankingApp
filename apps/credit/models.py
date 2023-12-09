import uuid
from django.db import models
from django.contrib.auth import get_user_model
from utils.models import HistorizedModel
from apps.account.models import CURRENCY_CHOICES, Account

USER_MODEL = get_user_model()

PAYMENT_CHOICES = (
    ("OY", "Once a year"),
    ("OM", "Once a month"),
)


class CreditDescription(HistorizedModel):
    description_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    duration_in_month = models.IntegerField()
    rate_index = models.DecimalField(max_digits=3, decimal_places=2)
    payment_type = models.CharField(max_length=64, choices=PAYMENT_CHOICES)


class Credit(HistorizedModel):
    credit_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name="credits")
    account_uuid = models.ForeignKey(Account, on_delete=models.PROTECT, null=False,
                                     blank=False, related_name="credits")
    description_uuid = models.ForeignKey(CreditDescription, on_delete=models.PROTECT, null=False,
                                         blank=False, related_name="credits")
    amount_to_pay = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=64, choices=CURRENCY_CHOICES, default="BYN")
    next_payout = models.DateTimeField(null=True)
    one_off_payment = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    one_off_current_payment = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    payout_count = models.IntegerField()
