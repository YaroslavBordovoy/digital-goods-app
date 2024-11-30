from django.contrib import admin
from django.urls import path

from digital_store.views import (
    IndexView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)

app_name = "digital_store"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("category/", CategoryListView.as_view(), name="category-list"),
    path("category/create/", CategoryCreateView.as_view(), name="category-create"),
    path("category/<int:pk>/update/", CategoryUpdateView.as_view(), name="category-update"),
    path("category/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category-delete"),
]
