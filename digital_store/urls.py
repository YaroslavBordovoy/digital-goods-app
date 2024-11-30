from django.contrib import admin
from django.urls import path

from digital_store.views import IndexView

app_name = "digital_store"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
