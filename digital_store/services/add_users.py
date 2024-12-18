import random

from faker import Faker

from accounts.models import User


fake = Faker()

def add_users():
    roles = ["SL"] * 1 + ["CS"] * 3
    user_objects = [
        User(
            username=fake.user_name(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            is_staff=False,
            is_active=True,
            role=random.choice(roles),
        )
        for _ in range(51)
    ]
    User.objects.bulk_create(user_objects)

    print("Users added successfully")
