from django.urls import path
from catalog.apps import CatalogConfig
from . import views
from .views import HomeView, ContactsView, ProductDetailView, ProductListView, CategoryProductsView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/', ProductListView.as_view(), name='product_list'),

    path('category/<int:category_id>/products/', CategoryProductsView.as_view(), name='category_products'),

    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    path('product/<int:pk>/unpublish/', views.ProductUnpublishView.as_view(), name='product_unpublish'),
    ]