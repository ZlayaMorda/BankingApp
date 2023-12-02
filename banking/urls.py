from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("", include("apps.home.urls")),
    path("admin/", admin.site.urls),
    path("account/", include("apps.account.urls")),
    path("auth/", include("apps.authorization.urls"))
]
