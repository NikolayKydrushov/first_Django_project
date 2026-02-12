from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


class OwnerRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки, что пользователь - владелец продукта"""

    def test_func(self):
        product = self.get_object()
        # Суперпользователь может всё
        if self.request.user.is_superuser:
            return True
        # Является ли пользователь владельцем
        return product.owner == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Вы не являетесь владельцем этого продукта')
            return redirect('catalog:product_detail', product_id=self.get_object().pk)
        return super().handle_no_permission()


class OwnerOrModeratorRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки, что пользователь - владелец или модератор"""

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        # Суперпользователь может всё
        if user.is_superuser:
            return True

        # Модератор может удалять
        if user.has_perm('catalog.delete_product'):
            return True

        # Владелец может редактировать и удалять
        return product.owner == user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'У вас нет прав для выполнения этого действия')
            return redirect('catalog:product_detail', product_id=self.get_object().pk)
        return super().handle_no_permission()