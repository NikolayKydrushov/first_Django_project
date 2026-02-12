from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import ProductForm, ProductModerationForm
from .mixins import (
    OwnerOrModeratorRequiredMixin,  # Импортируем миксины
    OwnerRequiredMixin,
)
from .models import Category, Product
from .services import ProductService


class HomeView(TemplateView):
    template_name = "catalog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Показываем только опубликованные продукты
        context["products"] = Product.objects.filter(status="published")
        context["title"] = "Skystore - Главная"
        return context


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        print(f"Новое сообщение от {name} ({email}): {message}")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    pk_url_kwarg = "product_id"
    login_url = "users:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        product = self.get_object()

        # Проверяем различные права для отображения кнопок
        context["is_owner"] = product.owner == user
        context["can_unpublish"] = user.has_perm("catalog.can_unpublish_product")
        context["can_delete"] = user.has_perm("catalog.delete_product")
        context["can_edit"] = context["is_owner"] or context["can_unpublish"]

        return context


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/products_list.html"
    context_object_name = "products"
    login_url = "users:login"

    def get_queryset(self):
        user = self.request.user

        # Модераторы видят все продукты
        if user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all()

        # Обычные пользователи видят свои продукты и опубликованные чужие
        return Product.objects.filter(
            models.Q(owner=user)  # Свои продукты
            | models.Q(status="published")  # Опубликованные чужие
        ).distinct()


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")
    login_url = "users:login"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Продукт сохраняется в form.save() с автоматической установкой владельца
        response = super().form_valid(form)
        messages.success(self.request, "Продукт успешно создан!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    """
    Обновление продукта - доступно только владельцу
    Модераторы НЕ могут редактировать чужие продукты
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("catalog:product_list")
    login_url = "users:login"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Продукт успешно обновлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, OwnerOrModeratorRequiredMixin, DeleteView):
    """
    Удаление продукта - доступно владельцу ИЛИ модератору
    """

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("catalog:product_list")
    login_url = "users:login"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        product_name = self.object.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Продукт "{product_name}" успешно удален!')
        return response


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Отмена публикации продукта - только для модераторов"""

    model = Product
    template_name = "catalog/product_confirm_unpublish.html"
    permission_required = "catalog.can_unpublish_product"
    login_url = "users:login"
    pk_url_kwarg = "pk"

    def get_success_url(self):
        return reverse_lazy(
            "catalog:product_detail", kwargs={"product_id": self.object.pk}
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = "draft"
        self.object.save()
        messages.success(request, f'Публикация продукта "{self.object.name}" отменена')
        return redirect(self.get_success_url())

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "У вас нет прав для отмены публикации")
            return redirect("catalog:product_detail", product_id=self.get_object().pk)
        return super().handle_no_permission()


class CategoryProductsView(LoginRequiredMixin, ListView):
    """
    Представление для отображения продуктов в указанной категории
    """
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    login_url = 'users:login'
    paginate_by = 9

    def get_queryset(self):
        """
        Получаем ID категории из URL и возвращаем продукты через сервисную функцию
        """
        category_id = self.kwargs.get('category_id')
        user = self.request.user

        # Используем сервисную функцию
        return ProductService.get_products_by_category_with_access(category_id, user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')

        try:
            context['category'] = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            context['category'] = None

        return context


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect("catalog:product_list")
