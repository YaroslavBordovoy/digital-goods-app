from django.urls import path, include

from accounts.views import register, activate

app_name = "accounts"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("activate/<str:uid>/<str:token>", activate, name="activate"),
]