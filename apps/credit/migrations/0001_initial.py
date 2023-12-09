# Generated by Django 4.2.7 on 2023-12-02 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("account", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CreditDescription",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "description_uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("duration_in_month", models.IntegerField()),
                ("rate_index", models.DecimalField(decimal_places=2, max_digits=3)),
                (
                    "payment_type",
                    models.CharField(
                        choices=[("OY", "Once a year"), ("OM", "Once a month")],
                        max_length=64,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Credit",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "credit_uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "amount_to_pay",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=14),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("BYN", "Belarusian Rubles"),
                            ("USD", "United States Dollar"),
                            ("EUR", "Euro"),
                        ],
                        default="BYN",
                        max_length=64,
                    ),
                ),
                ("next_payout", models.DateTimeField()),
                (
                    "one_off_payment",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=14),
                ),
                ("payout_count", models.IntegerField()),
                (
                    "account_uuid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="credits",
                        to="account.account",
                    ),
                ),
                (
                    "description_uuid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="credits",
                        to="credit.creditdescription",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="credits",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
