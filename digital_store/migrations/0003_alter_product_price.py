# Generated by Django 5.1.3 on 2024-12-18 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("digital_store", "0002_order_customer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]