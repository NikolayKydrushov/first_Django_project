from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Add test product to the database'

    def handle(self, *args, **kwargs):

        Product.objects.all().delete()
        Category.objects.all().delete()

        category1, _ = Category.objects.get_or_create(name='Одежда', description='Все для людей')
        category2, _ = Category.objects.get_or_create(name='Электроника', description='Техника')

        products = [
            {'name': 'Рубашка', 'description': 'Тонкий ткань', 'category': category1, 'purchase_price' : 1000},
            {'name': 'Худи', 'description': 'Согреет всегда', 'category': category1, 'purchase_price' : 5000},
            {'name': 'Джинсы', 'description': 'Синие', 'category': category1, 'purchase_price': 3500},
            {'name': 'Смартфон', 'description': 'Новый', 'category': category2, 'purchase_price': 45000},
            {'name': 'Ноутбук', 'description': 'Игровой', 'category': category2, 'purchase_price': 85000},
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'The product already exists: {product.name}'))