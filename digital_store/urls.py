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
    path("category/", CategoryListView.as_view(), name="category-list"),
    path(
        "category/create/",
        CategoryCreateView.as_view(),
        name="category-create"
    ),
    path(
        "category/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category-update"
    ),
    path(
        "category/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category-delete"
    ),
    path("product/", ProductListView.as_view(), name="product-list"),
    path(
        "product/<int:pk>",
        ProductDetailView.as_view(),
        name="product-detail"
    ),
    path(
        "product/create/",
        ProductCreateView.as_view(),
        name="product-create"
    ),
    path(
        "product/<int:pk>/update/",
        ProductUpdateView.as_view(),
        name="product-update"
    ),
    path(
        "product/<int:pk>/delete/",
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
    path("order/create/", OrderCreateView.as_view(), name="order-create"),
]
