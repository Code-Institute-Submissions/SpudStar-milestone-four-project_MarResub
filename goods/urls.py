from django.urls import path, include
from . import views

# Changes to URLs suggested by mentor to reduce clutter
urlpatterns = [
    path('', views.all_products, name='products'),
    path('detail/<int:product_id>/',
         views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/',
         views.delete_product, name='delete_product'),
]
