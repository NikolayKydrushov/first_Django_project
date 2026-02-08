from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'purchase_price', 'picture']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # 1. Поле "Наименование" (name)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control form-control-lg',  # CSS-классы для стилизации
            'placeholder': 'Введите название продукта',  # Текст подсказки
            'autofocus': 'autofocus',  # Автофокус на поле
        })
        self.fields['name'].label = 'Наименование *'
        self.fields['name'].help_text = ''

        # 2. Поле "Описание" (description)
        self.fields['description'].widget.attrs.update(attrs={
            'class': 'form-control',  # CSS-класс
            'placeholder': 'Опишите ваш продукт',  # Текст подсказки
            'rows': '5',  # Количество строк
            'style': 'resize: vertical;',  # Ограничение изменения размера
        })
        self.fields['description'].label = 'Описание'
        self.fields['description'].required = False  # Делаем необязательным
        self.fields['description'].help_text = ''

        # 3. Поле "Категория" (category)
        self.fields['category'].widget.attrs.update({
            'class': 'form-select',  # CSS-классы для select
        })
        self.fields['category'].label = 'Категория *'
        self.fields['category'].empty_label = '--- Выберите категорию ---'
        self.fields['category'].help_text = ''

        # 4. Поле "Цена" (purchase_price)
        self.fields['purchase_price'].widget.attrs.update({
            'class': 'form-control',  # CSS-класс
            'placeholder': '0.00',  # Текст подсказки
            'min': '0',  # Минимальное значение
            'step': '0.01',  # Шаг изменения
            'style': 'max-width: 200px;',  # Ограничение ширины
        })
        self.fields['purchase_price'].label = 'Цена за покупку *'
        self.fields['purchase_price'].help_text = 'Введите цену продукта. Цена должна быть в пределах от 0.01 до 1 000 000.'

        # 5. Поле "Фотография" (picture)
        self.fields['picture'].widget.attrs.update({
            'class': 'form-control',  # CSS-класс
            'accept': 'image/*',  # Разрешенные типы файлов
        })
        self.fields['picture'].label = 'Фотография'
        self.fields['picture'].help_text = 'Загрузите изображение продукта (JPG, PNG, GIF)'

    # Метод валидации названия
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if name is None:
            raise forms.ValidationError("Наименование обязательно для заполнения")

        name = name.strip()
        if not name:
            raise forms.ValidationError("Наименование не может состоять только из пробелов")

        # Список запрещенных слов прямо в методе
        forbidden_words = [
            'казино', 'криптовалюта', 'крипта', 'биржа',
            'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
        ]

        name_lower = name.lower()
        for word in forbidden_words:
            if word in name_lower:
                raise forms.ValidationError(f"Название содержит запрещенное слово: '{word}'")

        return name

    # Метод валидации описания
    def clean_description(self):
        description = self.cleaned_data.get('description')

        # Если description равен None, возвращаем пустую строку
        if description is None:
            return ''

        # Убираем пробелы
        description = description.strip()

        # Если после удаления пробелов строка пустая, возвращаем пустую строку
        if not description:
            return ''

        # Список запрещенных слов
        forbidden_words = [
            'казино', 'криптовалюта', 'крипта', 'биржа',
            'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
        ]

        description_lower = description.lower()
        for word in forbidden_words:
            if word in description_lower:
                raise forms.ValidationError(f"Описание содержит запрещенное слово: '{word}'")

        return description

    # Метод валидации цены
    def clean_purchase_price(self):
        """Валидация цены продукта - проверка, что цена не отрицательная"""
        price = self.cleaned_data.get('purchase_price')

        # Проверяем, что цена указана
        if price is None:
            raise forms.ValidationError("Цена обязательна для заполнения")

        # Проверяем, что цена не отрицательная
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной")

        # Проверка на слишком большую цену
        if price > 1000000:  # Максимум 1 миллион
            raise forms.ValidationError(
                "Цена слишком высокая. Максимальная цена - 1 000 000."
            )

        # Проверка на слишком маленькую цену
        if 0 < price < 0.01:  # Минимум 0.01
            raise forms.ValidationError(
                "Цена слишком низкая. Минимальная цена - 0.01."
            )

        return round(price, 2)
