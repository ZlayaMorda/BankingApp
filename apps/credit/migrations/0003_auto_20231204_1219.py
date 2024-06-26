# Generated by Django 4.2.7 on 2023-12-04 12:19

from django.db import migrations


def update_credits(apps, schema_editor):
    CreditDescription = apps.get_model("credit", "CreditDescription")
    CreditDescription.objects.filter(payment_type="('OM', 'Once a month')").update(payment_type="OM")
    CreditDescription.objects.filter(payment_type="('OY', 'Once a year')").update(payment_type="OY")


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0002_auto_20231202_1208'),
    ]

    operations = [
        migrations.RunPython(update_credits),
    ]
