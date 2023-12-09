from django.urls import path
from apps.credit import views

urlpatterns = [
    path("create/", views.CreditCreate.as_view(), name="credit_create"),
    path("ajax/load-payments", views.get_payment, name="ajax_load_payments")
]
