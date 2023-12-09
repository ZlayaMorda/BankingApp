from django.contrib import admin
from apps.credit.models import Credit, CreditDescription

admin.site.register(Credit)
admin.site.register(CreditDescription)
