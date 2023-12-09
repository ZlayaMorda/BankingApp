from django.urls import path
from apps.authorization import views

urlpatterns = [
    path("sign-up/", views.user_sign_up, name="sign_up"),
    path("sign-in/", views.user_sign_in, name="sign_in"),
    path("sign-in-code/", views.user_sign_in_code, name="sign_in_code"),
]
