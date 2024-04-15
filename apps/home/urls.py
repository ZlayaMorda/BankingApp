from django.urls import path
from apps.home import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]
