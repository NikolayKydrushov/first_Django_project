from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse


# Create your models here.



class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='наименование',
        help_text='введите наименование продукта'
    )
    description = models.CharField(
        max_length=100,
        verbose_name='описание',
    )
    picture = models.ImageField(
        upload_to= 'photos/',
        blank=True,
        null=True,
        verbose_name='фотография'
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name='наименование',
        null=True,
        blank=True,
        related_name='products'
    )
    purchase_price = models.FloatField(
        max_length=100,
        verbose_name='цена за покупку'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата последнего изменения'
    )
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('archived', 'В архиве'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='статус публикации'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # Если пользователь удален, владелец становится NULL
        null=True,
        blank=True,
        verbose_name='Владелец',
        related_name='products'  # Позволяет обращаться user.products.all()
    )


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[str(self.id)])

    # 1. Product:
    #     * наименование,
    #     * описание,
    #     * изображение,
    #     * категория,
    #     * цена за покупку,
    #     * дата создания,
    #     * дата последнего изменения.

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование', help_text='введите наименование категории')
    description = models.CharField(max_length=100, verbose_name='описание')

    def __str__(self):
        return self.name

    # 2.
    # Category:
    # *наименование,
    # *описание.

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
