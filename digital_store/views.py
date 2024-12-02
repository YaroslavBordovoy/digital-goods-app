from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from digital_store.forms import ProductCreateForm
from digital_store.models import Product, Category, Cart, Order, CartProduct, OrderProduct

User = get_user_model()
SELLER_PERMISSIONS = [
        "category.can_add_category",
        "category.can_edit_category",
        "category.can_delete_category",
        "product.can_add_product",
        "product.can_edit_product",
        "product.can_delete_product",
    ]

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


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = SELLER_PERMISSIONS
    model = Category
    fields = ("name", "description",)
    success_url = reverse_lazy("digital_store:category-list")

    def form_valid(self, form):
        form.instance.name = form.instance.name.lower().capitalize()
        messages.success(self.request, "You have successfully created a new category!")
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = SELLER_PERMISSIONS
    model = Category
    fields = ("name", "description",)
    success_url = reverse_lazy("digital_store:category-list")

    def form_valid(self, form):
        form.instance.name = form.instance.name.lower().capitalize()
        messages.success(self.request, "You have successfully updated the category!")
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = SELLER_PERMISSIONS
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


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = SELLER_PERMISSIONS
    model = Product
    form_class = ProductCreateForm

    def get_success_url(self):
        return reverse_lazy("digital_store:product-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = SELLER_PERMISSIONS
    model = Product
    form_class = ProductCreateForm

    def get_success_url(self):
        return reverse_lazy("digital_store:product-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = SELLER_PERMISSIONS
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


class CartAddView(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int, *args, **kwargs):
        product = get_object_or_404(Product, id=pk)
        cart, created = Cart.objects.get_or_create(customer=self.request.user)
        cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

        action = self.request.POST.get("action")

        if action == "increase":
            cart_product.quantity += 1
            cart_product.save()
        if action == "reduce":
            if cart_product.quantity > 1:
                cart_product.quantity -= 1
                cart_product.save()
            else:
                cart_product.delete()

        return redirect("digital_store:cart-list")


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order


class OrderCreateView(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, *args, **kwargs):
        cart = Cart.objects.get(customer=self.request.user)

        if cart.cart_items.exists():
            order = Order.objects.create()
            order_products = [
                OrderProduct(
                    product=item.product,
                    quantity=item.quantity,
                    order=order,
                )
                for item in cart.cart_items.all()
            ]
            OrderProduct.objects.bulk_create(order_products)

        CartProduct.objects.filter(cart__customer=self.request.user).delete()

        return redirect("digital_store:order-list")
