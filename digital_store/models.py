from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField(
        to="Category",
        related_name="category_products",
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller_products",
    )
    image = models.ImageField(upload_to="products/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_add_product", "Can add product"),
            ("can_edit_product", "Can edit product"),
            ("can_delete_product", "Can delete product"),
        ]

    def __str__(self) -> str:
        return f"Product: {self.name} (price: {self.price}, category: {self.category})"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "categories"
        ordering = ("name",)
        permissions = [
            ("can_add_category", "Can add category"),
            ("can_edit_category", "Can edit category"),
            ("can_delete_category", "Can delete category"),
        ]

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    class StatusChoice(models.TextChoices):
        PENDING = "PE", _("Pending")
        PROCESSING = "PR", _("Processing")
        COMPLETED = "CO", _("Completed")
        CANCELLED = "CA", _("Cancelled")
        REFUNDED = "RE", _("Refunded")

    products = models.ManyToManyField(
        to=Product,
        related_name="product_orders",
        through="OrderProduct",
    )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=2,
        choices=StatusChoice,
        default=StatusChoice.PENDING
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        default=1,
    )


class Cart(models.Model):
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    products = models.ManyToManyField(
        to=Product,
        related_name="product_carts",
        through="CartProduct",
    )

    def __str__(self) -> str:
        return f"User cart: {self.customer.username}"


class OrderProduct(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("product", "order",)


class CartProduct(models.Model):
    cart = models.ForeignKey(
        to=Cart,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("product", "cart",)
