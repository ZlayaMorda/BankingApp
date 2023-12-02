from django.urls import path
from apps.account import views


urlpatterns = [
    path("<uuid:pk>/", views.AccountDetailView.as_view(), name="account_detail"),
    path("list/", views.AccountListCreateView.as_view(), name="account_list")
]
