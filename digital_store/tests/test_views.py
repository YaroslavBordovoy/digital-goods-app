from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from digital_store.models import Category, Product, Order, OrderProduct, Cart, CartProduct


class IndexViewTest(TestCase):
    def test_context_data(self):
        get_user_model().objects.create(username="user1", role="CU")
        get_user_model().objects.create(username="user2", role="SL")
        Product.objects.create(name="Laptop", price=95, seller_id=2)
        response = self.client.get(reverse("digital_store:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["customer_amount"], 1)
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


    def test_create_category(self):
        response = self.client.post(reverse("digital_store:category-create"), {
            "name": "test1",
            "description": "test_description",
        })

        self.assertEqual(response.status_code, 302)  # Redirect after success

        category = Category.objects.get(name="Video Games")

        self.assertIsNotNone(category)
        self.assertEqual(category.description, "test_description")

    def test_update_category(self):
        user = get_user_model().objects.create_user(username="seller", role="SL")
        user.user_permissions.add(Permission.objects.get(codename="can_edit_category"))
        category = Category.objects.create(
            name="test_category",
            description="test_description",
        )
        self.client.force_login(user)
        response = self.client.post(
            reverse(
                "digital_store:category-update",
                args=[category.id]),
            {
                "name": "test_name",
                "description": "test_update_description",
            }
        )

        self.assertEqual(response.status_code, 302)

        category.refresh_from_db()

        self.assertEqual(category.name, "test_name")
        self.assertEqual(category.description, "test_update_description")

    def test_delete_category(self):
        user = get_user_model().objects.create_user(
            username="seller",
            role="SL",
        )

        user.user_permissions.add(
            Permission.objects.get(codename="can_delete_category")
        )
        category = Category.objects.create(name="test", description="test_description")
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("digital_store:category-delete", args=[self.category.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Category.objects.filter(id=category.id).exists())


class ProductViewsTests(TestCase):
    def setUp(self):
        self.seller = get_user_model().objects.create_user(username="seller", role="SL")
        self.seller.user_permissions.add(Permission.objects.get(codename="can_add_product"))
        self.seller.user_permissions.add(Permission.objects.get(codename="can_edit_product"))
        self.seller.user_permissions.add(Permission.objects.get(codename="can_delete_product"))

        self.category = Category.objects.create(name="Test category", description="Test description")

        self.product1 = Product.objects.create(name="product1", price=10, seller=self.seller)
        self.product2 = Product.objects.create(name="product2", price=20, seller=self.seller)

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

    def test_product_create_view(self):
        response = self.client.post(
            reverse("digital_store:product-create"),
            {
                "name": "test product",
                "price": 300,
                "description": "test_description",
                "category": [self.category.id],
            }
        )

        self.assertEqual(response.status_code, 302)

        product = Product.objects.get(name="test product")

        self.assertEqual(product.seller, self.seller)

    def test_product_update_view(self):
        response = self.client.post(
            reverse("digital_store:product-update", args=[self.product1.id]),
            {
                "name": "test_update",
                "price": 50,
                "description": "test_update_description",
                "category": [self.category.id],
            }
        )

        self.assertEqual(response.status_code, 302)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, "test_update")
        self.assertEqual(self.product1.price, 50)

    def test_product_delete_view(self):
        response = self.client.post(
            reverse("digital_store:product-delete", args=[self.product1.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(id=self.product1.id).exists())


class CartViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="customer", role="CU")
        self.product1 = Product.objects.create(name="product1", price=1000.00, seller=self.user)
        self.product2 = Product.objects.create(name="product2", price=500.00, seller=self.user)
        self.client.force_login(self.user)

        self.cart = Cart.objects.create(customer=self.user)
        CartProduct.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartProduct.objects.create(cart=self.cart, product=self.product2, quantity=3)

    def test_cart_view_context(self):
        response = self.client.get(reverse("digital_store:cart-list"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "product1")
        self.assertContains(response, "product2")

        total_price = (self.product1.price * 2) + (self.product2.price * 3)

        self.assertContains(response, f"Total price: {total_price}")

    def test_add_product_to_cart(self):
        response = self.client.post(
            reverse("digital_store:cart-add", args=[self.product1.id]),
            {"action": "increase"}
        )

        self.assertEqual(response.status_code, 302)

        cart_product = CartProduct.objects.get(cart=self.cart, product=self.product1)

        self.assertEqual(cart_product.quantity, 1)

    def test_increase_product_quantity_in_cart(self):
        CartProduct.objects.create(
            cart=self.cart,
            product=self.product1,
            quantity=1,
        )

        response = self.client.post(
            reverse("digital_store:cart-add", args=[self.product1.id]),
            {"action": "increase"}
        )

        self.assertEqual(response.status_code, 302)

        cart_product = CartProduct.objects.get(cart=self.cart, product=self.product1)

        self.assertEqual(cart_product.quantity, 2)

    def test_reduce_product_quantity_in_cart(self):
        CartProduct.objects.create(
            cart=self.cart,
            product=self.product1,
            quantity=2
        )

        response = self.client.post(
            reverse("digital_store:cart-add", args=[self.product1.id]),
            {"action": "reduce"}
        )

        self.assertEqual(response.status_code, 302)

        cart_product = CartProduct.objects.get(cart=self.cart, product=self.product1)

        self.assertEqual(cart_product.quantity, 1)

    def test_delete_product_from_cart(self):
        CartProduct.objects.create(
            cart=self.cart,
            product=self.product1,
            quantity=1
        )

        response = self.client.post(
            reverse("digital_store:cart-add", args=[self.product1.id]),
            {"action": "delete"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            CartProduct.objects.filter(cart=self.cart, product=self.product1).exists()
        )
