from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )

from blog.models import BlogPost


# Create your views here.

# Список всех записей
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Вывод опубликованных статей
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


# Детальный просмотр записи
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        # Получаем объект и увеличиваем счетчик просмотров
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


# Создание новой записи
class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = '/blog/'  # Можно использовать reverse, но его нет в списке разрешенных

    def form_valid(self, form):
        # Дополнительная логика при создании
        response = super().form_valid(form)
        return response


# Редактирование записи
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        # Возвращаем на страницу записи после редактирования
        return f'/blog/post/{self.object.pk}/'


# Удаление записи
class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = '/blog/'
