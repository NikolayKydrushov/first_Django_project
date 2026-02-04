from django.contrib import admin

from catalog.models import Product, Category


# Register your models here.

@admin.register(Category)
class CatalogAdmin(admin.ModelAdmin):
    # Для Category выведите id и name в списке.
    list_display = ("id", "name")
    list_filter = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Для Product выведите id и name, price и category в списке.
    # Настройте фильтрацию продуктов по категории.
    # Настройте поиск по полям name и description.
    list_display = ("id", "name", "purchase_price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")