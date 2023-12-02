import uuid
from django.db import models
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


CURRENCY_CHOICES = (
    ("BYN", "Belarusian Rubles"),
    ("USD", "United States Dollar"),
    ("EUR", "Euro"),
)


class Account(models.Model):
    account_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name='accounts')
    currency = models.CharField(max_length=64, choices=CURRENCY_CHOICES, default="BYN")
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
