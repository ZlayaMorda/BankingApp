from django.urls import path
from apps.credit import views

urlpatterns = [
    path("create/", views.CreditCreate.as_view(), name="credit_create"),
    path("ajax/load-payments", views.CreditLoadPayment.as_view(), name="ajax_load_payments"),
    path("ajax/load-durations", views.CreditLoadDuration.as_view(), name="ajax_load_durations"),
    path("ajax/load-rate-percent", views.RatePercentView.as_view(), name="ajax_load_rate_percent"),
    path("list/", views.CreditList.as_view(), name="credit_list"),
]
