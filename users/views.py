
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            send_mail(
                subject='Добро пожаловать!',
                message=f'Здравствуйте, {user.email}! Спасибо за регистрацию на нашем сайте.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('catalog:product_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """Авторизация пользователя"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {email}!')
                return redirect('catalog:product_list')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('catalog:product_list')