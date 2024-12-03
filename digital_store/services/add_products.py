import random

from django.contrib.auth import get_user_model

from digital_store.models import Category, Product


def add_products():
    categories = list(Category.objects.all())
    sellers = list(get_user_model().objects.filter(role="SL"))

    product_objects = [
        Product(
            name=f"product_{i + 1}",
            description=f"Description of product #{i + 1}",
            price=random.randint(150, 1000),
            seller=random.choice(sellers),
        )
        for i in range(37)
    ]

    products = Product.objects.bulk_create(product_objects)

    for product in products:
        product.category.add(random.choice(categories))

    print("Products created successfully")
