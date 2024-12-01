from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from digital_store.forms import ProductCreateForm
from digital_store.models import Product, Category, Cart, Order, CartProduct

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


class ProductListView(generic.ListView):
    model = Product
    queryset = Product.objects.select_related("seller").prefetch_related("category")
    paginate_by = 9


class ProductDetailView(generic.DetailView):
    model = Product


class ProductCreateView(generic.CreateView):
    model = Product
    form_class = ProductCreateForm

    def get_success_url(self):
        return reverse_lazy("digital_store:product-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductUpdateView(generic.UpdateView):
    model = Product
    form_class = ProductCreateForm

    def get_success_url(self):
        return reverse_lazy("digital_store:product-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductDeleteView(generic.DeleteView):
    model = Product
    success_url = reverse_lazy("digital_store:product-list")


class CartView(generic.TemplateView):
    template_name = "digital_store/cart_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(customer=self.request.user)

        cart_items = cart.cart_items.select_related("product")

        context["total_price"] = sum(
            item.product.price * item.quantity for item in cart_items
        )

        context["cart_items"] = cart_items

        return context


class CartAddView(generic.View):
    def post(self, request: HttpRequest, pk: int):
        product = get_object_or_404(Product, id=pk)
        cart, created = Cart.objects.get_or_create(customer=self.request.user)
        cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_product.quantity += 1
            cart_product.save()

        return redirect("digital_store:product-list")


