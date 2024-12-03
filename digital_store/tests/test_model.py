from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

from digital_store.models import Category, Product, Order, OrderProduct, Cart, CartProduct


SELLER = get_user_model().objects.create_user(
    username="test_seller",
    password="test_password",
)


class CategoryModelTests(TestCase):
    def test_category_str(self):
        category = Category.objects.create(name="test", description="First")

        self.assertEqual(str(category), category.name)

    def test_category_name_unique(self):
        Category.objects.create(name="Unique Name", description="First")
        with self.assertRaises(Exception):
            Category.objects.create(name="Unique Name", description="Second")

    def test_category_ordering(self):
        category1 = Category.objects.create(name="B Category", description="category1")
        category2 = Category.objects.create(name="A Category", description="category2")
        categories = Category.objects.all()

        self.assertEqual(list(categories), [category2, category1])

    def test_category_custom_permissions(self):
        permissions = [
            "can_add_category",
            "can_edit_category",
            "can_delete_category",
        ]
        for perm in permissions:
            self.assertTrue(Permission.objects.filter(codename=perm).exists())

    def test_category_create(self):
        Category.objects.create(name="New Category", description="Description")

        self.assertEqual(Category.objects.count(), 1)


class ProductModelTests(TestCase):
    def setUp(self) -> None:
        self.category1 = Category.objects.create(
            name="Test Category1",
            description="Test Description1",
        )
        self.category2 = Category.objects.create(
            name="Test Category2",
            description="Test Description2",
        )

    def test_product_str(self):
        product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=5.00,
            category=self.category1,
            seller=SELLER,
        )

        self.assertEqual(
            str(product),
            f"Product: {product.name} "
            f"(price: {product.price}, category: {product.category})",
        )

    def test_product_two_categories(self):
        product = Product.objects.create(
            name="Test Product",
            price=5.00,
            seller=SELLER,
        )
        product.category.add(self.category1, self.category2)

        self.assertEqual(product.category.count(), 2)

    def test_product_seller_relation(self):
        product = Product.objects.create(
            name="Test Product",
            price=5.00,
            seller=SELLER,
        )

        self.assertEqual(product.seller.username, "test_seller")

    def test_product_custom_permissions(self):
        permissions = [
            "can_add_product",
            "can_edit_product",
            "can_delete_product",
        ]
        for perm in permissions:
            self.assertTrue(Permission.objects.filter(codename=perm).exists())


class OrderModelTests(TestCase):
    def test_status_choices_and_default_status(self):
        expected_choices = [
            ("PE", "Pending"),
            ("PR", "Processing"),
            ("CO", "Completed"),
            ("CA", "Cancelled"),
            ("RE", "Refunded"),
        ]

        order = Order.objects.create()

        self.assertEqual(Order.StatusChoice.choices, expected_choices)
        self.assertEqual(order.status, Order.StatusChoice.PENDING)

    def test_status_update(self):
        order = Order.objects.create()
        order.status = Order.StatusChoice.COMPLETED
        order.save()

        self.assertEqual(order.status, Order.StatusChoice.COMPLETED)

    def test_products_relation(self):
        product1 = Product.objects.create(name="Test prod1", price=100, seller=SELLER)
        product2 = Product.objects.create(name="Test prod2", price=50, seller=SELLER)
        order = Order.objects.create()
        OrderProduct.objects.create(order=order, product=product1, quantity=1)
        OrderProduct.objects.create(order=order, product=product2, quantity=2)

        self.assertEqual(order.products.count(), 2)
        self.assertIn(product1, order.products.all())
        self.assertIn(product2, order.products.all())

    def test_order_product_relationship(self):
        product = Product.objects.create(name="Test prod", price=50, seller=SELLER)
        order = Order.objects.create()
        order_product = OrderProduct.objects.create(
            order=order,
            product=product,
            quantity=3
        )

        self.assertEqual(order_product.order, order)
        self.assertEqual(order_product.product, product)
        self.assertEqual(order_product.quantity, 3)


class CartModelTests(TestCase):
    def test_default_quantity(self):
        cart = Cart.objects.create(user=seller)
        product = Product.objects.create(name="Test product", price=50, seller=SELLER)
        cart_product = CartProduct.objects.create(cart=cart, product=product)

        self.assertEqual(cart_product.quantity, 1)
