from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView, DetailView, ListView

from .models import Product, Category


# Create your views here.

# Контроллер главной страницы
class HomeView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['title'] = 'Skystore - Главная'
        return context

    # def post(self, request, *args, **kwargs):
    #     return HttpResponse("Метод не поддерживается", status=405)


# Контроллер страницы контактов (с обработкой POST)
class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"Новое сообщение от {name} ({email}): {message}")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено. Мы свяжемся с вами по {email}.")


# Контроллер деталей продуктов
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

# CreateView, ListView, DetailView, UpdateView, DeleteView

# Контроллер списка продуктов
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'

