from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Контроллер главной страницы
def home(request):
    if request.method == 'GET':
        return render(request, 'catalog/home.html')
    else:
        return HttpResponse("Метод не поддерживается", status=405)

# Контроллер страницы контактов (с обработкой POST)
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"Новое сообщение от {name} ({email}): {message}")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено. Мы свяжемся с вами по {email}.")
    elif request.method == 'GET':
        return render(request, 'catalog/contacts.html')
    else:
        return HttpResponse("Метод не поддерживается", status=405)
