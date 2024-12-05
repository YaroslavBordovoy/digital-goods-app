import django
import django_filters
from django.forms import Select

from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
        label="Min price",
        widget=django.forms.NumberInput(attrs={'placeholder': 'Enter min price'})
    )
    price_max = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
        label="Max price",
        widget=django.forms.NumberInput(attrs={'placeholder': 'Enter max price'})
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label="Category",
        empty_label="Select a category",
    )

    class Meta:
        model = Product
        fields = ("price_min", "price_max", "category",)
