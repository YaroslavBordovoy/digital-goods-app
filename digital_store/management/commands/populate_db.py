from django.core.management.base import BaseCommand

from digital_store.services.add_category import add_category, CATEGORIES
from digital_store.services.add_products import add_products
from digital_store.services.add_users import add_users


class Command(BaseCommand):
    help = "Populate the database with categories"

    def handle(self, *args, **kwargs):
        add_category(CATEGORIES)
        add_users()
        add_products()
