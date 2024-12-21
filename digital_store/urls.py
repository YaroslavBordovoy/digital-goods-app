from django.urls import path

from digital_store.views import (
    IndexView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    CartView,
    CartAddView,
    OrderListView,
    OrderCreateView,
)


app_name = "digital_store"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path(
        "categories/create/",
        CategoryCreateView.as_view(),
        name="category-create"
    ),
    path(
        "categories/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category-update"
    ),
    path(
        "categories/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category-delete"
    ),
    path("products/", ProductListView.as_view(), name="product-list"),
    path(
        "products/<int:pk>",
        ProductDetailView.as_view(),
        name="product-detail"
    ),
    path(
        "products/create/",
        ProductCreateView.as_view(),
        name="product-create"
    ),
    path(
        "products/<int:pk>/update/",
        ProductUpdateView.as_view(),
        name="product-update"
    ),
    path(
        "products/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product-delete"
    ),
    path("cart/", CartView.as_view(), name="cart-list"),
    path("cart/<int:pk>/add/", CartAddView.as_view(), name="cart-add"),
    path(
        "cart/<int:pk>/quantity-change/",
        CartAddView.as_view(),
        name="cart-quantity-change"
    ),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
]
