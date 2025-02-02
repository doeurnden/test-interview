from django.urls import path
from .views import category_list, category_detail, product_list, product_detail, search_products_by_image

urlpatterns = [
    path('categories/', category_list, name='category-list'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),

    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),

    path('search-by-image/', search_products_by_image, name='search-by-image'),
]