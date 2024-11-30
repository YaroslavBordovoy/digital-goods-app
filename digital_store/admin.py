from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from digital_store.models import Order, Cart, Category, Product, OrderProduct
from accounts.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("role",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info", {
                "fields": ("first_name", "last_name", "role",)
            }
        ),
    )
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "price",
        "display_category",
        "seller",
        "created_at",
        "updated_at",
    )
    search_fields = ("name",)
    list_filter = ("seller", "category",)
    list_per_page = 20

    def display_category(self, obj):
        return ", ".join(category.name for category in obj.category.all())

    display_category.short_description = "Category"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("capitalize_name", "description",)

    def capitalize_name(self, obj):
        return obj.name.capitalize()

    capitalize_name.short_description = "Name"


class OrderProductInLine(admin.TabularInline):
    model = OrderProduct
    autocomplete_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "display_product_name",
        "display_customer",
        "order_date",
        "status",
    )
    inlines = (OrderProductInLine, )
    list_filter = ("status",)
    list_per_page = 20

    def display_product_name(self, obj):
        return ", ".join(
            [
                f"{product.product.name} (x{product.quantity})"
                for product in obj.order_products.all()
            ]
        )

    def display_customer(self, obj):
        return obj.cart.customer.username

    display_product_name.short_description = "Product name"
    display_customer.short_description = "Customer"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "display_products"
    )
    list_per_page = 20

    def display_products(self, obj):
        orders = obj.orders.all()
        order_details = []
        for order in orders:
            products = [order_product.product.name for order_product in order.order_products.all()]
            order_details.append(f"Order ID: {order.id} - Products: {', '.join(products)}")
        return "\n".join(order_details)

    display_products.short_description = "Products in Order"
