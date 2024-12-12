from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from decimal import Decimal

from digital_store.models import Category, Product, Order, Cart, CartProduct


class IndexViewTest(TestCase):
    def test_context_data(self):
        get_user_model().objects.create(username="user1", role="CU")
        get_user_model().objects.create(username="user2", role="SL")
        Product.objects.create(name="Laptop", price=Decimal("95"), seller_id=2)
        response = self.client.get(reverse("digital_store:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["customer_amount"], 2)
        self.assertEqual(response.context["seller_amount"], 1)
        self.assertEqual(response.context["product_amount"], 1)


class CategoryViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="seller",
            role="SL"
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename="can_add_category")
        )
        self.client.force_login(self.user)

    def test_category_list_view(self):
        Category.objects.create(name="category1", description="description1")
        Category.objects.create(name="category2", description="description2")
        response = self.client.get(reverse("digital_store:category-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "category1")
        self.assertContains(response, "category2")

    def test_update_category(self):
        user = get_user_model().objects.create_user(username="seller2", role="SL")
        user.user_permissions.add(Permission.objects.get(codename="can_edit_category"))
        category = Category.objects.create(
            name="test_category",
            description="test_description",
        )
        self.client.force_login(user)

        self.assertEqual(category.name, "test_category")
        self.assertEqual(category.description, "test_description")


class ProductViewsTests(TestCase):
    def setUp(self):
        self.seller = get_user_model().objects.create_user(username="seller", role="SL")
        self.seller.user_permissions.add(Permission.objects.get(codename="can_add_product"))
        self.seller.user_permissions.add(Permission.objects.get(codename="can_edit_product"))
        self.seller.user_permissions.add(Permission.objects.get(codename="can_delete_product"))

        self.category = Category.objects.create(name="Test category", description="Test description")

        self.product1 = Product.objects.create(name="product1", price=Decimal("10"), seller=self.seller)
        self.product2 = Product.objects.create(name="product2", price=Decimal("20"), seller=self.seller)

        self.client.force_login(self.seller)

    def test_product_list_view(self):
        response = self.client.get(reverse("digital_store:product-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "product1")
        self.assertContains(response, "product2")

    def test_product_detail_view(self):
        response = self.client.get(
            reverse("digital_store:product-detail", args=[self.product1.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "product1")
        self.assertContains(response, "10")


class OrderViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="customer", role="CU"
        )
        self.product1 = Product.objects.create(
            name="product1",
            price=Decimal("500"),
            seller=self.user
        )
        self.product2 = Product.objects.create(
            name="product2",
            price=Decimal("200"),
            seller=self.user
        )
        self.client.force_login(self.user)

        self.cart = Cart.objects.create(customer=self.user)
        self.cart_item1 = CartProduct.objects.create(
            cart=self.cart,
            product=self.product1,
            quantity=1,
        )
        self.cart_item2 = CartProduct.objects.create(
            cart=self.cart,
            product=self.product2,
            quantity=2,
        )

    def test_order_list_view(self):
        Order.objects.create()
        response = self.client.get(reverse("digital_store:order-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order")
