from django import forms
from django.contrib.auth import get_user_model

from digital_store.models import Product, Category


class ProductCreateForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Product
        fields = ("name", "description", "price", "category", "image",)
