import random

from django.contrib.auth import get_user_model

from digital_store.models import Category, Product


def add_products() -> None:
    categories = list(Category.objects.all())
    sellers = list(get_user_model().objects.filter(role="SL"))

    product_objects = [
        Product(
            name=f"product_{i + 1}",
            description=f"Description of product #{i + 1}",
            price=round(random.uniform(100.00, 999.99), 2),
            seller=random.choice(sellers),
        )
        for i in range(37)
    ]

    products = Product.objects.bulk_create(product_objects)

    product_categories = [
        product.category.through(product_id=product.id, category_id=random.choice(categories).id)
        for product in products
    ]

    Product.category.through.objects.bulk_create(product_categories)

    print("Products created successfully")
