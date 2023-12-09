from django.urls import path
from apps.account import views


urlpatterns = [
    path("<uuid:pk>/", views.AccountDetailView.as_view(), name="account_detail"),
    path("list/", views.AccountListView.as_view(), name="account_list"),
    path("transfer/<uuid:pk>/", views.AccountTransferView.as_view(), name="account_transfer"),
    path("create/", views.AccountCreateView.as_view(), name="account_create"),
    path("delete/<uuid:pk>/", views.AccountDeleteView.as_view(), name="account_delete"),
    path("change-for-token/<uuid:pk>/", views.AccountTokenView.as_view(), name="change_for_token"),
]
