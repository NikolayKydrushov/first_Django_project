from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с email в качестве основного идентификатора
    """
    # Основные поля
    email = models.EmailField(
        'электронная почта',
        unique=True,
        help_text='Обязательное поле. Используется для входа в систему.'
    )

    # Дополнительные поля по заданию
    avatar = models.ImageField(
        'аватар',
        upload_to='users/avatars/',
        blank=True,
        null=True,
        help_text='Загрузите изображение для аватара'
    )

    phone_number = models.CharField(
        'номер телефона',
        max_length=15,
        blank=True,
        null=True,
        help_text='Введите номер телефона'
    )

    country = models.CharField(
        'страна',
        max_length=100,
        blank=True,
        null=True,
        help_text='Укажите страну проживания'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email


