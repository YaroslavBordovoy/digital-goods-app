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


class CategoryTests(TestCase):
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
