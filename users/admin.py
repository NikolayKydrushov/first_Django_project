from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # Для CustomUser выводим email, username, phone_number и country в списке
    list_display = ("id", "email", "phone_number", "country",)

    # Настраиваем фильтрацию пользователей по стране и статусу staff
    list_filter = ("email", "phone_number", "country")
