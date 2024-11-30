from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from digital_store.models import Product, Category


User = get_user_model()

class IndexView(generic.TemplateView):
    template_name = "digital_store/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["customer_amount"] = User.objects.count()
        context["seller_amount"] = User.objects.filter(role="SL").count()
        context["product_amount"] = Product.objects.count()

        return context


class CategoryListView(generic.ListView):
    model = Category


class CategoryCreateView(generic.CreateView):
    model = Category
    fields = ("name", "description",)
    success_url = reverse_lazy("digital_store:category-list")

    def form_valid(self, form):
        form.instance.name = form.instance.name.lower().capitalize()
        messages.success(self.request, "You have successfully created a new category!")
        return super().form_valid(form)


class CategoryUpdateView(generic.UpdateView):
    model = Category
    fields = ("name", "description",)
    success_url = reverse_lazy("digital_store:category-list")

    def form_valid(self, form):
        form.instance.name = form.instance.name.lower().capitalize()
        messages.success(self.request, "You have successfully updated the category!")
        return super().form_valid(form)


class CategoryDeleteView(generic.DeleteView):
    model = Category
    success_url = reverse_lazy("digital_store:category-list")

    def form_valid(self, form):
        messages.success(self.request, "You have successfully deleted the category!")
        return super().form_valid(form)



