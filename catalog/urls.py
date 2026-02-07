from django.urls import path
# from catalog.apps import CatalogConfig
# from . import views
from .views import HomeView, ContactsView, ProductDetailView, ProductListView

# app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
path('products/', ProductListView.as_view(), name='product_list'),
    ]