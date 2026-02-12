from django.core.cache import cache
from django.views.generic import ListView
from django.db import models
from .models import Product, Category


class ProductService:
    """Сервисный класс для работы с продуктами"""

    @staticmethod
    def get_products_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
            return Product.objects.filter(category=category)
        except Category.DoesNotExist:
            return Product.objects.none()

    @staticmethod
    def get_products_by_category_with_access(category_id, user):
        try:
            category = Category.objects.get(id=category_id)
            products = Product.objects.filter(category=category)

            if not (user and user.has_perm('catalog.can_unpublish_product')):
                products = products.filter(
                    models.Q(status='published') |
                    models.Q(owner=user)
                ).distinct()

            return products
        except Category.DoesNotExist:
            return Product.objects.none()


class CachedProductListView(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Ключ для кеша
        cache_key = 'all_products_list'

        # Пробуем получить из кеша
        queryset = cache.get(cache_key)

        # Если в кеше нет - получаем из БД и сохраняем в кеш
        if not queryset:
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, 60 * 15)  # 15 минут

        return queryset