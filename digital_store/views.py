from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from digital_store.models import Product


User = get_user_model()


class IndexView(generic.TemplateView):
    template_name = "digital_store/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer_amount"] = User.objects.count()
        context["seller_amount"] = User.objects.filter(role="SL").count()
        context["product_amount"] = Product.objects.count()

        return context