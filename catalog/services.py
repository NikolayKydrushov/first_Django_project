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