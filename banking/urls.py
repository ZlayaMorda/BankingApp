from django.contrib import admin
from django.urls import path, include
from banking import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", views.home, name="home"),
    path("account/", include("apps.account.urls")),
    path("", include("apps.authorization.urls"))
]
