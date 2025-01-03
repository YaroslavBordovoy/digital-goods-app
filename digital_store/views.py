from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django_filters.views import FilterView

from digital_store.filters import ProductFilter
from digital_store.forms import ProductCreateForm, ProductCategorySearchForm
from digital_store.models import (
    Product,
    Category,
    Cart,
    Order,
    CartProduct,
    OrderProduct
)


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
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = ProductCategorySearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = Category.objects.all()
        form = ProductCategorySearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class CategoryCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    permission_required = SELLER_PERMISSIONS
    model = Category
    fields = ("name", "description",)
    success_url = reverse_lazy("digital_store:category-list")

    def form_valid(self, form):
        form.instance.name = form.instance.name.lower().capitalize()
        messages.success(
            self.request,
            "You have successfully created a new category!"
        )
        return super().form_valid(form)


class CategoryUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    permission_required = SELLER_PERMISSIONS
    model = Category
    fields = ("name", "description",)
    success_url = reverse_lazy("digital_store:category-list")

    def form_valid(self, form):
        form.instance.name = form.instance.name.lower().capitalize()
        messages.success(
            self.request,
            "You have successfully updated the category!"
        )
        return super().form_valid(form)


class CategoryDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    permission_required = SELLER_PERMISSIONS
    model = Category
    success_url = reverse_lazy("digital_store:category-list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "You have successfully deleted the category!"
        )
        return super().form_valid(form)


class ProductListView(FilterView):
    model = Product
    paginate_by = 12
    filterset_class = ProductFilter
    template_name = "digital_store/product_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = ProductCategorySearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = Product.objects.select_related(
            "seller"
        ).prefetch_related("category")
        form = ProductCategorySearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class ProductDetailView(generic.DetailView):
    model = Product


class ProductCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    permission_required = SELLER_PERMISSIONS
    model = Product
    form_class = ProductCreateForm

    def get_success_url(self):
        return reverse_lazy("digital_store:product-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    permission_required = SELLER_PERMISSIONS
    model = Product
    form_class = ProductCreateForm

    def get_success_url(self):
        return reverse_lazy("digital_store:product-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    permission_required = SELLER_PERMISSIONS
    model = Product
    success_url = reverse_lazy("digital_store:product-list")


class CartView(LoginRequiredMixin, generic.TemplateView):
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
        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart,
            product=product
        )

        action = self.request.POST.get("action")

        if action == "increase":
            cart_product.quantity += 1
            cart_product.save()
        elif action == "reduce":
            if cart_product.quantity > 1:
                cart_product.quantity -= 1
                cart_product.save()
            else:
                cart_product.delete()
        elif action == "delete":
            cart_product.delete()

        return redirect("digital_store:cart-list")


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class OrderCreateView(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, *args, **kwargs):
        cart = Cart.objects.get(customer=self.request.user)

        if cart.cart_items.exists():
            order = Order.objects.create(customer=self.request.user)
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
