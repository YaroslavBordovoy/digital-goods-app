from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class UserRole(models.TextChoices):
        CUSTOMER = "CS", _("Customer")
        SELLER = "SL", _("Seller")

    role = models.CharField(
        max_length=2,
        choices=UserRole,
        default=UserRole.CUSTOMER
    )

